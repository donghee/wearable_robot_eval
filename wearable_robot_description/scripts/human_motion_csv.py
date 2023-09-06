#!/usr/bin/env python

import rclpy
from rclpy.node import Node
import tf2_ros
#from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped, Quaternion, PoseStamped
from std_srvs.srv import Empty
from rclpy.qos import QoSProfile

import math
import json
import os, glob
import time
import numpy as np

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

        self.in_dir = self.declare_parameter("in_dir", "./motions").value
        self.out_dir = self.declare_parameter("out_dir", "./motions/converted").value
        self.speed = self.declare_parameter("speed", 0.01).value
        self.store_converted = self.declare_parameter("store_converted", False).value

        self.files = []
        file_query = os.path.join(self.in_dir, "*.txt")
        for file in glob.glob(file_query):
            self.files.append(file)
            print(file)
        self.current_file_index = 0
        self.file_count = len(self.files)

        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        qos_profile = QoSProfile(depth=10)
        self.state = self.create_publisher(JointState, 'joint_states', qos_profile)

        self.load_next_json()

    def load_next_json(self):
        path = self.files[self.current_file_index]

        with open(path) as f:
            lines = f.read()

        self.obj = json.loads(lines)
        self.num_frames = len(self.obj['Frames'])
        self.obj['converted'] = []
        self.obj['file_path'] = path

        dir_name, file_name = os.path.split(path)
        self.obj['save_path'] = os.path.join(self.out_dir, file_name)
        self.obj['source_name'] = file_name
        #print(list(map(sum, zip(*self.obj['Frames'])))[0])
        self.obj['duration_in_seconds'] = list(map(sum, zip(*self.obj['Frames'])))[0]

        self.get_logger().info("Loaded file %s with %i Frames" % (path, self.num_frames))

        self.current_file_index += 1

    def quat_to_euler(self, w,x,y,z):
        q = []
        if w < 0:
            q = [-x, -y, -z, -w]
        else:
            q = [x, y, z, w]
        #(r,p,y) = euler_from_quaternion(q, axes='rxyz')
        (r,p,y) = euler_from_quaternion(q)
        return [r,p,y]

    def get_joint_state(self, frame):
        s = JointState()
        s.header.stamp = self.get_clock().now().to_msg()

        chest_rotation = self.quat_to_euler(frame[7],frame[8],frame[9],frame[10])
        neck_rotation = self.quat_to_euler(frame[11],frame[12],frame[13],frame[14])
        right_hip_rotation = self.quat_to_euler(frame[15],frame[16],frame[17],frame[18])
        right_knee_rotation = self.quat_to_euler(frame[19],frame[20],frame[21],frame[22])[0]
        right_ankle_rotation = self.quat_to_euler(frame[23],frame[24],frame[25],frame[26])
        right_shoulder_rotation = self.quat_to_euler(frame[27],frame[28],frame[29],frame[30])
        right_elbow_rotation = self.quat_to_euler(frame[31],frame[32],frame[33],frame[34])[0]
        left_hip_rotation = self.quat_to_euler(frame[35],frame[36],frame[37],frame[38])
        left_knee_rotation = self.quat_to_euler(frame[39],frame[40],frame[41],frame[42])[0]
        left_ankle_rotation = self.quat_to_euler(frame[43],frame[44],frame[45],frame[46])
        left_shoulder_rotation = self.quat_to_euler(frame[47],frame[48],frame[49],frame[50])
        left_elbow_rotation = self.quat_to_euler(frame[51],frame[52],frame[53],frame[54])[0]
        
        s.name = [
            "j_root_chest_joint1",
            "j_root_chest_joint2",
            "j_root_chest_joint3",
            "j_chest_neck_joint1",
            "j_chest_neck_joint2",
            "j_chest_neck_joint3",
            "j_root_right_hip_joint1",
            "j_root_right_hip_joint2",
            "j_root_right_hip_joint3",
            "j_right_knee",
            "j_right_knee_right_ankle_joint1",
            "j_right_knee_right_ankle_joint2",
            "j_right_knee_right_ankle_joint3",
            "j_chest_right_shoulder_joint1",
            "j_chest_right_shoulder_joint2",
            "j_chest_right_shoulder_joint3",
            "j_right_elbow",
            "j_root_left_hip_joint1",
            "j_root_left_hip_joint2",
            "j_root_left_hip_joint3",
            "j_left_knee",
            "j_left_knee_left_ankle_joint1",
            "j_left_knee_left_ankle_joint2",
            "j_left_knee_left_ankle_joint3",
            "j_chest_left_shoulder_joint1",
            "j_chest_left_shoulder_joint2",
            "j_chest_left_shoulder_joint3",
            "j_left_elbow"
        ]

        s.position = [
            chest_rotation[0],
            chest_rotation[1],
            chest_rotation[2],
            neck_rotation[0],
            neck_rotation[1],
            neck_rotation[2],
            right_hip_rotation[0],
            right_hip_rotation[1],
            right_hip_rotation[2],
            right_knee_rotation,
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
            left_knee_rotation,
            left_ankle_rotation[0],
            left_ankle_rotation[1],
            left_ankle_rotation[2],
            left_shoulder_rotation[0],
            left_shoulder_rotation[1],
            left_shoulder_rotation[2],
            left_elbow_rotation
        ]

        return s

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

    def store_frame(self, frame, t, s, transform):
        pos = transform.transform.translation
        rot = transform.transform.rotation
        
        arr = [
            frame[0],
            pos.x,
            pos.y,
            pos.z,
            rot.x,
            rot.y,
            rot.z,
            rot.w
        ]

        arr.extend(s.position)

        self.obj['converted'].append(arr)

    def store_current(self):
        if not self.store_converted:
            return

        self.obj['Frames'] = None
        json_string = json.dumps(self.obj)
        with open(self.obj['save_path'], "w") as f:
            f.write(json_string)
        
        self.get_logger().info("Saving to %s" % self.obj['save_path'])

    def process_frame(self, t):
        frame = self.obj['Frames'][t]

        s = self.get_joint_state(frame)
        tr = self.get_robot_base_pose(frame)
        self.state.publish(s)
        self.tf_broadcaster.sendTransform(tr)

        #self.store_frame(frame, t, s, tr)

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
                    self.store_current()
                    stop = True

            if self.file_count - 1 > self.current_file_index:
                self.load_next_json()
                counter = 0
                stop = False
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

