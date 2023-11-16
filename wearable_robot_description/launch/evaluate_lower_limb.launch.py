from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    control_type_arg = DeclareLaunchArgument(
            'control_type',
            default_value='normal',
            description='Control algorithm for lower limb wearable device'
            )
    return LaunchDescription([
        control_type_arg,
        Node(
            package='wearable_robot_description',
            executable='human_motion_csv_gz_toz_export.py',
            name='human_gait_position_test_node',
            parameters=[{'control_type': LaunchConfiguration('control_type')}]
        )
    ])
