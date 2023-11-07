#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time
import math

from sensor_msgs.msg import JointState
from geometry_msgs.msg import WrenchStamped

class HumanArmEffortTestNode(Node):

    def __init__(self):
        super().__init__('human_arm_effort_test_node')
        self.reference_motions_one_cycle = []
        self.cnt = 0
        self.FREQ = 500

        self.reference_motions_one_cycle = self.init_reference_motion("sine")
        #  self.reference_motions_one_cycle = self.init_reference_motion("triangle")

        # current arm joint angle
        self.arm_joint_position = 0.0
        self.arm_joint_torque = 0.0
        self.arm_joint_motor_torque = 0.0

        self.joint_state_subscription = self.create_subscription(
                JointState,
                'joint_states',
                self.listener_joint_state_callback,
                10)

        # PI Controller: error
        self.error = 0.0
        self.error_cum = 0.0
        self.error_prev = 0.0

        self.publisher_ = self.create_publisher(Float64MultiArray, '/forward_command_controller/commands', 10)
        self.pid_control_timer = self.create_timer(1.0/self.FREQ, self.pid_control_callback)

        # init torque command of left elbow joint
        commands = Float64MultiArray()
        commands.data.append(100.0)

        # read device torque
        self.device_torques = []
        self.filtered_device_torque = 0.0

        self.wrench_subscription = self.create_subscription(
                WrenchStamped,
                '/upper_limb/wrench',
                self.listener_upper_limb_wrench_callback,
                10)

    def init_reference_motion(self, motion_type):
        x = 0.0
        reference_motions = []

        if motion_type == 'triangle':
            # triangle wave
            for i in range(self.FREQ*2*2): # flexion and extension
                if i < self.FREQ*2:
                    x += 90/(self.FREQ*2) # flextion
                else:
                    x -= 90/(self.FREQ*2) # extension
                reference_motions.append(math.radians(x))

        if motion_type == 'sine':
            # sine wave
            for i in range(self.FREQ*2*2):
                reference_motions.append(math.pi/2*math.sin(2.0 * math.pi * i / (self.FREQ*2*2*2.0)))

        return reference_motions

    def listener_joint_state_callback(self, msg):
        if msg.name == ['j_left_elbow']:
            self.arm_joint_position = msg.position[0]
            #  self.get_logger().info(f'Received joint states: {self.arm_joint_position}')

    def listener_upper_limb_wrench_callback(self, msg):
        #self.get_logger().info(f'Received upper_limb torque: {msg.wrench.torque}')
        self.device_torques.append(msg.wrench.torque.x)
        #print(self.device_torques)

        if len(self.device_torques) > 750: # window size 750. 1.5 sec delayed
            self.device_torques.pop(0)

        self.filtered_device_torque = sum(self.device_torques) / len(self.device_torques)
        #print(f"self.filtered_device_torque: {self.filtered_device_torque}")


    def pid_control_callback(self):
        # triangle wave motion's pid
        kP = 20.0
        kI = 0.02
        kD = 0.2
        C = 0.0

        # sine wave motion's pid: no wearable
        kP = 20.0
        kI = 0.15
        kD = 0.2
        C = 0.0

        # sine wave motion's pid: with wearable device
        kP = 40.0
        kI = 0.15
        kD = 20.0
        C = 0.0

        if self.cnt > self.FREQ*2*2 * 10:
            commands = Float64MultiArray()
            commands.data.append(0.0)
            self.publisher_.publish(commands)
            print(f"stopped! reference motion: {self.arm_joint_position}, {0.0} ")
            return

        current_reference_position = self.reference_motions_one_cycle[self.cnt % (self.FREQ*2*2)] 
        self.error = self.arm_joint_position - current_reference_position
        self.error_cum += self.error
        error_diff = self.error - self.error_prev
        self.error_prev = self.error

        # output
        human_torque = (kP * self.error) + (kI * self.error_cum) - C + (kD * error_diff)

        # publish human torque
        commands = Float64MultiArray()

        # with external torque 
        # TODO: check the direction of torque
        human_torque = human_torque - self.filtered_device_torque

        commands.data.append(-human_torque)
        self.publisher_.publish(commands)

        # logging
        phase = "flexion" if self.cnt % (self.FREQ*2*2) < self.FREQ*2 else "extension"
        print(f"human {phase}: {round(math.degrees(current_reference_position),1)}, {round(math.degrees(self.arm_joint_position),1)}, {-human_torque} ")
       
        self.cnt += 1

    def reset_torque(self):
        commands = Float64MultiArray()
        commands.data.append(0.0)
        self.publisher_.publish(commands)

def main(args=None):
    rclpy.init(args=args)

    effort_test_node = HumanArmEffortTestNode()

    try:    
        rclpy.spin(effort_test_node)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        effort_test_node.reset_torque()
    finally:
        effort_test_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
