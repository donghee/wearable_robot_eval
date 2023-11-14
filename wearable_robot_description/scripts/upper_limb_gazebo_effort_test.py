#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time
import math
import csv

from sensor_msgs.msg import JointState
from geometry_msgs.msg import WrenchStamped

class UpperLimbEffortTestNode(Node):
    def __init__(self):
        super().__init__('upper_limb_effort_test_node')
        self.FREQ = 500
        self.DEVICE_FLEXION_TORQUE = 5.0
        self.DEVICE_EXTENSION_TORQUE = 1.0

        self.arm_joint_position = 0.0
        self.joint_state_subscription = self.create_subscription(
                JointState,
                'joint_states',
                self.listener_joint_state_callback,
                10)

        self.device_arm_joint_torque = 0.0
        self.upper_limb_wrench_subscription = self.create_subscription(
                WrenchStamped,
                '/upper_limb/wrench',
                self.listener_upper_limb_wrench_callback,
                10)
        
        self.human_arm_joint_torque_cmd = 0.0
        self.hubman_elbow_joint_torque_subscription = self.create_subscription(
                Float64MultiArray, 
                '/forward_command_controller/commands', 
                self.listener_human_elbow_joint_torque_callback,
                10)

        # set initial phase and device torque
        self.phase = "flexion"
        self.device_torque = -self.DEVICE_FLEXION_TORQUE
        self.last_valid_device_torque = self.device_torque

        # control type: "square_wave", "square_wave_failed", "zero"
        self.control_type = "square_wave" # default control type is square_wave
        control_type_parameter = self.declare_parameter('control_type').get_parameter_value().string_value
        if control_type_parameter in ['square_wave', 'square_wave_failed', 'zero']:
            self.control_type = control_type_parameter
        else:
            self.control_type = 'zero'
        self.get_logger().info("Control type: %s" % self.control_type)

        self.publisher_ = self.create_publisher(Float64MultiArray, '/upper_limb_forward_command_controller/commands', 10)
        self.control_timer = self.create_timer(1.0/self.FREQ, self.control_callback)

        commands = Float64MultiArray()
        commands.data.append(100.0)

        # export data
        self.start_time = self.get_clock().now()
        self.device_arm_joint_torque_cmd = 0.0
        self.export_data_timer = self.create_timer(1.0/30.0, self.export_data_callback)

        with open('/tmp/interaction-upper.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timer", "State", "InteractionTorque", "Angle", "MotorTorque", "HumanTorque"
            ])

        with open('/tmp/wearability-upper.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timer", "Angle"
            ])


        with open('/tmp/visualization-upper.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Chest_x", "Chest_y", "Chest_z",
                "Neck_x", "Neck_y", "Neck_z",
                "Rhip_x", "Rhip_y", "Rhip_z",
                "Rknee_z",
                "Rankle_x", "Rankle_y" , "Rankle_z",
                "Rshoulder_x", "Rshoulder_y", "Rshoulder_z",
                "Relbow_z",
                "Lhip_x", "Lhip_y", "Lhip_z",
                "Lknee_z",
                "Lankle_x", "Lankle_y" , "Lankle_z",
                "Lshoulder_x", "Lshoulder_y", "Lshoulder_z",
                "Lelbow_z",
                "Safety_Score"
            ])

    def export_data_callback(self):
        current_time = self.get_clock().now()
        elapsed_time = current_time - self.start_time
        elapsed_seconds = elapsed_time.nanoseconds / 1e9

        with open('/tmp/interaction-upper.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            data_row = [elapsed_seconds, self.phase, self.device_arm_joint_torque,
                        math.degrees(self.arm_joint_position), self.device_arm_joint_torque_cmd,
                        self.human_arm_joint_torque_cmd
                        ]
            writer.writerow(data_row)


        with open('/tmp/wearability-upper.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            data_row = [elapsed_seconds, -(math.degrees(self.arm_joint_position)-180)]
            writer.writerow(data_row)

        with open('/tmp/visualization-upper.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            data_row = [0.0, 0.0, 0.0, 
                        0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0,
                        -10.0,
                        0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0,
                        0.0,
                        0.0, 0.0, 0.0,
                        78.0, # TODO: change model's axis direction
                        0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0,
                        round(math.degrees(self.arm_joint_position), 2),
                        0.25
                        ]
            writer.writerow(data_row)


    def listener_joint_state_callback(self, msg):
        if msg.name == ['arm_joint']:
            self.arm_joint_position = -msg.position[0] - math.radians(90.0)

    def listener_upper_limb_wrench_callback(self, msg):
        self.device_arm_joint_torque = msg.wrench.torque.x

    def listener_human_elbow_joint_torque_callback(self, msg):
        self.human_arm_joint_torque_cmd = msg.data[0]

    def square_wave_torque_control(self):
        if self.phase == "extension":
            if self.arm_joint_position < (math.radians(0.0) + 0.04):
                self.device_torque = -self.DEVICE_FLEXION_TORQUE
                self.last_valid_device_torque = self.device_torque
                self.phase = "flexion"
        elif self.phase == "flexion":
            if self.arm_joint_position > (math.radians(90.0) - 0.15):
                self.device_torque = self.DEVICE_EXTENSION_TORQUE
                self.last_valid_device_torque = self.device_torque
                self.phase = "extension"

    def square_wave_torque_failed_control(self):
        self.square_wave_torque_control()

        # omit the device torque when the arm joint is in the range of 45 to 60 degrees
        if math.radians(45.0) < self.arm_joint_position and self.arm_joint_position < math.radians(60.0):
            self.device_torque = 0.0
        else:
            self.device_torque = self.last_valid_device_torque

    def zero_torque_control(self):
        self.square_wave_torque_control()
        self.device_torque = 0

    def control_callback(self):
        if self.control_type == "square_wave":
            self.square_wave_torque_control()
        elif self.control_type == "square_wave_failed":
            self.square_wave_torque_failed_control()
        elif self.control_type == "zero":
            self.zero_torque_control()

        # publish device torque
        commands = Float64MultiArray()
        commands.data.append(self.device_torque)
        self.publisher_.publish(commands)
        self.device_arm_joint_torque_cmd = self.device_torque

        print(f"device {self.phase}: {self.arm_joint_position}, {self.device_torque} ")

    def reset_torque(self):
        commands = Float64MultiArray()
        commands.data.append(0.0)
        self.publisher_.publish(commands)

def main(args=None):
    rclpy.init(args=args)

    effort_test_node = UpperLimbEffortTestNode()

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
