#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_wearable_robot_gazebo = get_package_share_directory('wearable_robot_gazebo')
    pkg_wearable_robot_description = get_package_share_directory('wearable_robot_description')

    # Start World
    start_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_wearable_robot_gazebo, 'launch', 'start_world_launch.py'),
        )
    )

    spawn_human_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_wearable_robot_description, 'launch', 'human_45dof.launch.py'),
        )
    ) 

    #  spawn_lower_limb_world = IncludeLaunchDescription(
    #      PythonLaunchDescriptionSource(
    #          os.path.join(pkg_wearable_robot_description, 'launch', 'lower_limb.launch.py'),
    #      )
    #  )

    evaluate_lower_limb = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_wearable_robot_description, 'launch', 'evaluate_lower_limb.launch.py'),
        )
    ) 

    return LaunchDescription([
        start_world,
        #  spawn_human_world,
        #  TimerAction(period=0.1, actions = [spawn_lower_limb_world]),
        TimerAction(period=3.0, actions = [evaluate_lower_limb]),
    ])
