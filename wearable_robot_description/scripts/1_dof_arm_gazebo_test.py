#! /usr/bin/env python3

import sys
import rclpy
from rclpy.duration import Duration
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
import time

# ros2 action list -t
# ros2 action info /joint_trajectory_controller/follow_joint_trajectory -t
# ros2 interface show control_msgs/action/FollowJointTrajectory

class OneDofArmActionClient(Node):

    def __init__(self):
        super().__init__('one_dof_arm_actionclient')
        self._action_client = ActionClient(self, FollowJointTrajectory, '/joint_trajectory_controller/follow_joint_trajectory')
        self.goal_order = 0

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
            self.send_goal(-1.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 1:
            self.send_goal(-3.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 2:
            self.send_goal(-1.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 3:
            self.send_goal(-3.0)
            self.goal_order = self.goal_order + 1
            return

        if self.goal_order == 4:
            self.send_goal(-1.0)
            self.get_logger().info("상지 동작 수행 완료")

        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback:'+str(feedback))


def main(args=None):
    
    rclpy.init()

    action_client = OneDofArmActionClient()

    angle = float(sys.argv[1])
    action_client.send_goal(angle)

    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
