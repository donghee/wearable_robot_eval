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
            os.path.join(pkg_wearable_robot_description, 'launch', 'human_only.launch.py'),
        )
    )     

    spawn_eduexo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_wearable_robot_description, 'launch', 'eduexo_only.launch.py'),
        )
    )     

    test_eduexo_0 = launch_ros.actions.Node(
            package='wearable_robot_description',
            #executable=os.path.join(pkg_wearable_robot_description, 'scripts', '1_dof_arm_gazebo_test.py'),
            executable='1_dof_arm_gazebo_test.py',
            arguments=['-2.8'],
            output='screen',
        )
 
    test_eduexo_1 = launch_ros.actions.Node(
            package='wearable_robot_description',
            #executable=os.path.join(pkg_wearable_robot_description, 'scripts', '1_dof_arm_gazebo_test.py'),
            executable='1_dof_arm_gazebo_test.py',
            arguments=['-1.0'],
            output='screen',
        )
 
    test_eduexo_2 = launch_ros.actions.Node(
            package='wearable_robot_description',
            #executable=os.path.join(pkg_wearable_robot_description, 'scripts', '1_dof_arm_gazebo_test.py'),
            executable='1_dof_arm_gazebo_test.py',
            arguments=['-2.8'],
            output='screen',
        )
 
    test_eduexo_3 = launch_ros.actions.Node(
            package='wearable_robot_description',
            #executable=os.path.join(pkg_wearable_robot_description, 'scripts', '1_dof_arm_gazebo_test.py'),
            executable='1_dof_arm_gazebo_test.py',
            arguments=['-1.0'],
            output='screen',
        )
 
    test_eduexo_4 = launch_ros.actions.Node(
            package='wearable_robot_description',
            #executable=os.path.join(pkg_wearable_robot_description, 'scripts', '1_dof_arm_gazebo_test.py'),
            executable='1_dof_arm_gazebo_test.py',
            arguments=['-2.8'],
            output='screen',
        )
 
    test_eduexo_5 = launch_ros.actions.Node(
            package='wearable_robot_description',
            #executable=os.path.join(pkg_wearable_robot_description, 'scripts', '1_dof_arm_gazebo_test.py'),
            executable='1_dof_arm_gazebo_test.py',
            arguments=['-1.0'],
            output='screen',
        )

    return LaunchDescription([
        start_world,
        spawn_human,
        launch.actions.TimerAction(
            actions=[spawn_eduexo],
            period = 40.0
        ),
        ExecuteProcess(
            cmd=["ls", "-al"], output="screen"
        ),
        launch.actions.TimerAction(
            actions=[launch.actions.LogInfo(msg="Wait For The Right Arm's Oscillation to Stabilize!")],
            period = 5.0
        ),
        launch.actions.TimerAction(
            actions=[test_eduexo_0],
            period = 45.0
        ),
        launch.actions.TimerAction(
            actions=[test_eduexo_1],
            period = 50.0
        ),
        launch.actions.TimerAction(
            actions=[test_eduexo_2],
            period = 55.0
        ),
        launch.actions.TimerAction(
            actions=[test_eduexo_3],
            period = 60.0
        ),
        launch.actions.TimerAction(
            actions=[test_eduexo_4],
            period = 65.0
        ),
        launch.actions.TimerAction(
            actions=[test_eduexo_5],
            period = 70.0
        )
    ])
