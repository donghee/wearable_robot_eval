import os
from ament_index_python.packages import get_package_prefix
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro

def generate_launch_description():
    pkg_wearable_robot_path = get_package_share_path('wearable_robot_description')

    default_model_path = pkg_wearable_robot_path / 'urdf/human_66dof.xacro'
    default_rviz_config_path = pkg_wearable_robot_path / 'rviz/urdf.rviz'

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    pkg_wearable_robot_description = get_package_share_directory('wearable_robot_description')

    install_dir = get_package_prefix('wearable_robot_description')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] =  os.environ['GAZEBO_MODEL_PATH'] + ':' + install_dir + '/share'
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  install_dir + "/share"

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'


    robot_description_config = xacro.process_file(str(default_model_path))
    robot_desc = robot_description_config.toxml()

    #print(robot_desc)

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher'
    )

    joint_state_broadcaster_node = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    joint_trajectory_controller_node = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_trajectory_controller"],
        output="screen",
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(package='wearable_robot_description', executable='spawn_entity.py', arguments=[robot_desc], output='screen'),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[
                {"robot_description": robot_desc}],
            output="screen"),
        joint_state_publisher_node,
        joint_state_broadcaster_node,
        joint_trajectory_controller_node,
    ])

