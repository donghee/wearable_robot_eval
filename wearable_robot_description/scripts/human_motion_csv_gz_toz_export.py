#!/usr/bin/python3.8

import rclpy
from rclpy.node import Node
import tf2_ros
#from tf.transformations import *
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TransformStamped, Quaternion, PoseStamped
from std_srvs.srv import Empty
from rclpy.qos import QoSProfile

import math
import json
import os, glob
import time
import numpy as np

import csv

def euler_to_quaternion(x, y, z):
    """
    Convert Euler angles (in radians) to Quaternion.
    Rotation order is x-y-z.
    """
    cx = math.cos(x * 0.5)
    sx = math.sin(x * 0.5)
    cy = math.cos(y * 0.5)
    sy = math.sin(y * 0.5)
    cz = math.cos(z * 0.5)
    sz = math.sin(z * 0.5)
    
    q_w = cx * cy * cz + sx * sy * sz
    q_x = sx * cy * cz - cx * sy * sz
    q_y = cx * sy * cz + sx * cy * sz
    q_z = cx * cy * sz - sx * sy * cz
    
    return (q_w, q_x, q_y, q_z)

def euler_from_quaternion(q):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    x = q[0]
    y = q[1]
    z = q[2]
    w = q[3]
    
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z # in radians

class Animator(Node):
    def __init__(self):
        super().__init__('animator')
        self.speed = self.declare_parameter("speed", 0.005).value

        # control type: "normal", "torque_limit", "rom_limit"
        control_type_parameter = self.declare_parameter('control_type').get_parameter_value().string_value
        self.motion_file = "/tmp/human_controller1_normal.txt"
        if control_type_parameter  == "normal":
            self.motion_file = "/tmp/human_controller1_normal.txt"
        elif control_type_parameter  == "torque_limit":
            self.motion_file = "/tmp/human_controller2_torqueLimit.txt"
        elif control_type_parameter  == "rom_limit":
            self.motion_file = "/tmp/human_controller3_romLimit.txt"

        self.get_logger().info("Control Type: %s" % control_type_parameter)
        self.get_logger().info("Motion File: %s" % self.motion_file)

        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        qos_profile = QoSProfile(depth=10)
        self.commands = self.create_publisher(Float64MultiArray, '/forward_position_controller/commands', qos_profile)

        #self.load_next_json()
        self.load_json()

        with open('/tmp/visualization-lower.csv', 'w', newline='') as file:
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

    def load_json(self):
        with open(self.motion_file) as f:
            lines = f.read()

        self.obj = json.loads(lines)
        self.num_frames = len(self.obj['Frames'])
        self.get_logger().info("Loaded file %s with %i Frames" % (self.motion_file, self.num_frames))

    def quat_to_euler(self, w,x,y,z):
        q = []
        if w < 0:
            q = [-x, -y, -z, -w]
        else:
            q = [x, y, z, w]
        #(r,p,y) = euler_from_quaternion(q, axes='rxyz')
        (r,p,y) = euler_from_quaternion(q)
        return [r,p,y]

    def get_joint_commands(self, frame):
        c = Float64MultiArray()

        chest_rotation = self.quat_to_euler(frame[7],frame[8],frame[9],frame[10])
        neck_rotation = self.quat_to_euler(frame[11],frame[12],frame[13],frame[14])
        right_hip_rotation = self.quat_to_euler(frame[15],frame[16],frame[17],frame[18])
        right_knee_rotation = self.quat_to_euler(frame[19],frame[20],frame[21],frame[22])[2]
        right_ankle_rotation = self.quat_to_euler(frame[23],frame[24],frame[25],frame[26])
        right_shoulder_rotation = self.quat_to_euler(frame[27],frame[28],frame[29],frame[30])
        right_elbow_rotation = self.quat_to_euler(frame[31],frame[32],frame[33],frame[34])[2]
        left_hip_rotation = self.quat_to_euler(frame[39],frame[40],frame[41],frame[42])
        left_knee_rotation = self.quat_to_euler(frame[43],frame[44],frame[45],frame[46])[2]
        left_ankle_rotation = self.quat_to_euler(frame[47],frame[48],frame[49],frame[50])
        left_shoulder_rotation = self.quat_to_euler(frame[51],frame[52],frame[53],frame[54])
        left_elbow_rotation = self.quat_to_euler(frame[55],frame[56],frame[57],frame[58])[2]
        
        c.data = [
            chest_rotation[0],
            chest_rotation[1],
            chest_rotation[2],
            neck_rotation[0],
            neck_rotation[1],
            neck_rotation[2],
            right_hip_rotation[0],
            right_hip_rotation[1],
            right_hip_rotation[2],
            right_knee_rotation - math.radians(10), # TODO: change model's axis direction
            right_ankle_rotation[0],
            right_ankle_rotation[1],
            right_ankle_rotation[2],
            right_shoulder_rotation[0],
            right_shoulder_rotation[1],
            right_shoulder_rotation[2],
            right_elbow_rotation,
            left_hip_rotation[0],
            left_hip_rotation[1],
            left_hip_rotation[2],
            left_knee_rotation + math.radians(60.0), # TODO: change model's axis direction
            left_ankle_rotation[0],
            left_ankle_rotation[1],
            left_ankle_rotation[2],
            left_shoulder_rotation[0],
            left_shoulder_rotation[1],
            left_shoulder_rotation[2],
            left_elbow_rotation
        ]
        c.data = [round(x, 2) for x in c.data]

        return c

    def get_robot_base_pose(self, frame):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "map"
        t.child_frame_id = "base_link"
        t.transform.translation.x = frame[0]
        t.transform.translation.y = -frame[2]
        t.transform.translation.z = frame[1]
        t.transform.rotation.w = frame[3]
        t.transform.rotation.x = frame[4]
        t.transform.rotation.y = -frame[6]
        t.transform.rotation.z = frame[5]
        return t

    def process_frame(self, t):
        frame = self.obj['Frames'][t]

        c = self.get_joint_commands(frame)

        with open('/tmp/visualization-lower.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            data_row = [round(math.degrees(x), 2) for x in c.data]
            data_row.append(0.25) # safe score
            writer.writerow(data_row)
        
        tr = self.get_robot_base_pose(frame)
        self.commands.publish(c)
        self.tf_broadcaster.sendTransform(tr)

        return frame[0]

    def spin_once(self):
        counter = 0
        self.process_frame(counter)

    def spin(self):
        counter = 0
        stop = False
        while rclpy.ok():
            while not stop:
                sleep_duration = self.process_frame(counter)
                time.sleep(sleep_duration * self.speed)

                counter += 1

                if counter == self.num_frames:
                    stop = True
            else:
                self.get_logger().info("Finished with all files")
                break

def main():
    rclpy.init()
    animator = Animator()

#    animator.spin_once()

    try:
       animator.spin()
    except KeyboardInterrupt:
       pass

    animator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

