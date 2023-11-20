#! /usr/bin/env python

import sys
import rclpy
from rclpy.duration import Duration
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

# ros2 action list -t
# ros2 action info /joint_trajectory_controller/follow_joint_trajectory -t
# ros2 interface show control_msgs/action/FollowJointTrajectory

import pyfirmata
from tkinter import *
 
board = pyfirmata.Arduino('/dev/ttyACM0')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
pin9 = board.get_pin('d:9:s')

def move_servo(a):
    pin9.write(a)
 
class OneDofArmActionClient(Node):

    def __init__(self):
        super().__init__('one_dof_arm_actionclient')
        self._action_client = ActionClient(self, FollowJointTrajectory, '/joint_trajectory_controller/follow_joint_trajectory')

    def send_goal(self, angle):
        goal_msg = FollowJointTrajectory.Goal()

        # Fill in data for trajectory
        joint_names = ["arm_joint"]

        points = []
        point1 = JointTrajectoryPoint()
        point1.positions = [1.8]

        point2 = JointTrajectoryPoint()
        point2.time_from_start = Duration(seconds=1, nanoseconds=0).to_msg()
        point2.positions = [angle]

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
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        #self.get_logger().info('Received feedback:'+str(feedback))


def main(args=None):
    rclpy.init()

    action_client = OneDofArmActionClient()
    angle = float(sys.argv[1])
    action_client.send_goal(angle)

    move_servo(int((angle - 2.0)  * 50))

    rclpy.spin(action_client)


def move_servo2(angle):
    action_client = OneDofArmActionClient()
    action_client.send_goal(float(angle))

    rclpy.spin_once(action_client)

    a = int((float(angle) -2.0) * 50)
    pin9.write(a)
 
def gui():
    root = Tk()
    rclpy.init()
    scale = Scale(root,
        command = move_servo2,
        from_ = 2.0,
        to = 6.0,
        resolution= 0.01,
        orient = HORIZONTAL,
        length = 400,
        label = 'Angle')

    scale.pack(anchor = CENTER)

    root.mainloop()

if __name__ == '__main__':
    #main()
    gui()
