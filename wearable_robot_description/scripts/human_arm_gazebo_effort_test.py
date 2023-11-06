#! /usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time
import math

from sensor_msgs.msg import JointState

class EffortTestNode(Node):

    def __init__(self):
        super().__init__('effort_test_node')
        # init reference motion
        self.reference_motions_one_cycle = []
        self.reference_motion_x = 0.0
        self.cnt = 0
        self.FREQ = 500

        # triangle wave
        #  for i in range(self.FREQ*2*2):
        #      # flextion
        #      if i < self.FREQ*2:
        #          self.reference_motion_x += 90/(self.FREQ*2)
        #      # extension
        #      else:
        #          self.reference_motion_x -= 90/(self.FREQ*2)
        #      self.reference_motions_one_cycle.append(math.radians(self.reference_motion_x))
        #      #  self.reference_motions_one_cycle.append(self.reference_motion_x)
        #  print(self.reference_motions_one_cycle)

        # sine wave
        for i in range(self.FREQ*2*2):
            self.reference_motions_one_cycle.append(math.sin(2.0 * math.pi * i / (self.FREQ*2*2*2.0)))

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
        self.get_logger().info('node created')
        
        self.pid_control_timer = self.create_timer(1.0/self.FREQ, self.pid_control_callback)

        # init torque command:
        # left elbow angle
        commands = Float64MultiArray()
        commands.data.append(100.0)

    def listener_joint_state_callback(self, msg):
        if msg.name == ['j_left_elbow']:
            self.arm_joint_position = msg.position[0]
            #  self.get_logger().info(f'Received joint states: {self.arm_joint_position}')

    def pid_control_callback(self):
        # triangle reference pid
        kP = 20.0
        kI = 0.02
        kD = 0.2
        C = 0.0

        # sinewave reference pid
        kP = 20.0
        kI = 0.15
        kD = 0.2
        C = 0.0

        if self.cnt > self.FREQ*2*2 * 10:
            commands = Float64MultiArray()
            commands.data.append(0.0)
            self.publisher_.publish(commands)
            return

        self.error = self.arm_joint_position - self.reference_motions_one_cycle[self.cnt % (self.FREQ*2*2)] 
        self.error_cum += self.error
        error_diff = self.error - self.error_prev
        self.error_prev = self.error

        # output
        human_torque = (kP * self.error) + (kI * self.error_cum) - C + (kD * error_diff)

        # publish human torque
        commands = Float64MultiArray()
        commands.data.append(-human_torque)
        self.publisher_.publish(commands)

        #  print("i: %d" % (self.cnt % (self.FREQ*2*2)))
        #  print("r_motion: %f" % self.reference_motions_one_cycle[self.cnt % (self.FREQ*2*2)])
        self.cnt += 1

def main(args=None):
    rclpy.init(args=args)

    effort_test_node = EffortTestNode()

    rclpy.spin(effort_test_node)
    effort_test_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
