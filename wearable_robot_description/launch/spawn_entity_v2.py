#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import rclpy
from gazebo_msgs.srv import SpawnEntity

def main(args=None):
    name = sys.argv[1]
    content = sys.argv[2]
    x = sys.argv[3]
    y = sys.argv[4]
    z = sys.argv[5]
 
    print(x,y,z)

    rclpy.init()
    node = rclpy.create_node('minimal_client_' + name)
    cli = node.create_client(SpawnEntity, '/spawn_entity')

    req = SpawnEntity.Request()
    req.name = name
    req.xml = content
    req.robot_namespace = ""
    req.reference_frame = "world"
    req.initial_pose.position.x = float(x)
    req.initial_pose.position.y = float(y)
    req.initial_pose.position.z = float(z)

    while not cli.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('service not available, waiting again...')

    future = cli.call_async(req)
    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        node.get_logger().info(
            'Result ' + str(future.result().success) + " " + future.result().status_message)
    else:
        node.get_logger().info('Service call failed %r' % (future.exception(),))

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
