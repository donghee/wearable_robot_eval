#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import TimerAction
from launch.actions import ExecuteProcess
import launch_ros.actions
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import launch.actions


def generate_launch_description():

    pkg_wearable_robot_gazebo = get_package_share_directory('wearable_robot_gazebo')
    pkg_wearable_robot_description = get_package_share_directory('wearable_robot_description')

    # Start World
    start_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_wearable_robot_gazebo, 'launch', 'start_world_launch.py'),
        )
    )

    spawn_human = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_wearable_robot_description, 'launch', 'human_45dof.launch.py'),
        )
    )     

    spawn_upper_limb = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_wearable_robot_description, 'launch', 'upper_limb.launch.py'),
        )
    )     

    test_upper_limb = launch_ros.actions.Node(
            package='wearable_robot_description',
            #executable=os.path.join(pkg_wearable_robot_description, 'scripts', '1_dof_arm_gazebo_test.py'),
            executable='upper_limb_gazebo_test.py',
            arguments=['-2.8'],
            output='screen',
        )

    return LaunchDescription([
        start_world,
        spawn_human,
        launch.actions.TimerAction(
            actions=[spawn_upper_limb],
            period = 5.0
        ),
        launch.actions.TimerAction(
            actions=[test_upper_limb],
            period = 10.0
        ),
        launch.actions.TimerAction(
            actions=[launch.actions.LogInfo(msg="상지 동작 수행 완료")],
            period = 72.0
        )
    ])
