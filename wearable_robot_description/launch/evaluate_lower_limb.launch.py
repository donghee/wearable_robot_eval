from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='wearable_robot_description',
            executable='human_motion_csv_gz_toz_export.py',
            name='human_gait_position_test_node'
        ),
    ])
