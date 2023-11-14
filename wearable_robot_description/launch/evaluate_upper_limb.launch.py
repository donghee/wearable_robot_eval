from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    control_type_arg = DeclareLaunchArgument(
            'control_type',
            default_value='square_wave',
            description='Control algorithm for upper limb wearable device'
            )
    return LaunchDescription([
        control_type_arg,
        Node(
            package='wearable_robot_description',
            executable='human_arm_gazebo_effort_test.py',
            name='human_arm_effort_test_node'
        ),
        Node(
            package='wearable_robot_description',
            executable='upper_limb_gazebo_effort_test.py',
            name='upper_limb_effort_test_node',
            parameters=[{'control_type': LaunchConfiguration('control_type')}]
        )
    ])
