#! /usr/bin/env python3

import sys
import rclpy
from rclpy.duration import Duration
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

import time
from sensor_msgs.msg import JointState
from geometry_msgs.msg import WrenchStamped
import csv
import math
import random

from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
# ros2 action list -t
# ros2 action info /joint_trajectory_controller/follow_joint_trajectory -t
# ros2 interface show control_msgs/action/FollowJointTrajectory

class OneDofArmActionClient(Node):

    def __init__(self):
        super().__init__('eduexo_arm_actionclient')
        self.goal_order = 0
        self.arm_joint_position = 0.0
        self.arm_joint_torque = 0.0
        self.arm_joint_motor_torque = 0.0
        self.joint_state_subscription = self.create_subscription(
                JointState,
                'joint_states',
                self.listener_joint_state_callback,
                10)

        self.wrench_subscription = self.create_subscription(
                WrenchStamped,
                '/eduexo/wrench',
                self.listener_wrench_callback,
                10)

        self.start_time = self.get_clock().now()
        self.export_csv_timer = self.create_timer(1.0/30.0, self.export_csv_callback)
        self.state = "extension"

        with open('/tmp/interaction.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timer", "State", "InteractionTorque", "Angle", "MotorTorque"
            ])

        self._action_client = ActionClient(self, FollowJointTrajectory, '/eduexo_joint_controller/follow_joint_trajectory')

        self.arm_joint_motor_torque = 1.0
        self.state = "flextion"
        self.send_goal(-3.0)

    def listener_joint_state_callback(self, msg):
        #self.get_logger().info(f'Received joint states: {msg}')
        if msg.name == ['arm_joint']:
            self.arm_joint_position = msg.position[0]

    def listener_wrench_callback(self, msg):
        #self.get_logger().info(f'Received wrench torque: {msg.wrench.torque}')
        self.arm_joint_torque = msg.wrench.torque.x

    def export_csv_callback(self):
        current_time = self.get_clock().now()
        elapsed_time = current_time - self.start_time
        elapsed_seconds = elapsed_time.nanoseconds / 1e9

        with open('/tmp/interaction.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            data_row = [elapsed_seconds, self.state, self.arm_joint_torque,
                        math.degrees(self.arm_joint_position)+270, self.arm_joint_motor_torque]
            writer.writerow(data_row)

    def send_goal(self, angle):
        goal_msg = FollowJointTrajectory.Goal()

        # Fill in data for trajectory
        joint_names = ["arm_joint"]

        points = []
        point1 = JointTrajectoryPoint()
        point1.positions = [1.8]
        #point1.velocities = [0.0]

        point2 = JointTrajectoryPoint()
        point2.time_from_start = Duration(seconds=1, nanoseconds=0).to_msg()
        point2.positions = [angle]
        #point2.velocities = [angle]

        #points.append(point1)
        points.append(point2)

        goal_msg.goal_time_tolerance = Duration(seconds=1, nanoseconds=0).to_msg()
        goal_msg.trajectory.joint_names = joint_names
        goal_msg.trajectory.points = points

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
    
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: '+str(result))
        time.sleep(3)
        if self.goal_order == 0:
            self.state = "extension"
            self.arm_joint_motor_torque = -1.0 + ((random.random() - 0.5 )/4.0)
            self.send_goal(-1.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 1:
            self.state = "flextion"
            self.arm_joint_motor_torque = 1.0 + ((random.random() - 0.5 )/4.0)
            self.send_goal(-3.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 2:
            self.state = "extension"
            self.arm_joint_motor_torque = -1.0 + ((random.random() - 0.5 )/4.0)
            self.send_goal(-1.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 3:
            self.state = "flextion"
            self.arm_joint_motor_torque = 1.0 + ((random.random() - 0.5 )/4.0)
            self.send_goal(-3.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 4:
            self.state = "extension"
            self.arm_joint_motor_torque = -1.0 + ((random.random() - 0.5 )/4.0)
            self.send_goal(-1.0)
            self.get_logger().info("상지 동작 수행 완료")
            rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        #self.get_logger().info('Received feedback:'+str(feedback))


def main(args=None):
    
    rclpy.init()

    action_client = OneDofArmActionClient()

    rclpy.spin(action_client)

    #  action_client.destory_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
