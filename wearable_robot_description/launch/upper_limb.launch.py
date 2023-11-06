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
import launch.actions
from launch.actions import ExecuteProcess

import xacro

def generate_launch_description():
    pkg_wearable_robot_path = get_package_share_path('wearable_robot_description')
    one_dof_arm_model_path = pkg_wearable_robot_path / 'urdf/upper_limb.xacro'
    default_rviz_config_path = pkg_wearable_robot_path / 'rviz/urdf.rviz'
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    install_dir = get_package_prefix('wearable_robot_description')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] =  os.environ['GAZEBO_MODEL_PATH'] + ':' + install_dir + '/share'
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  install_dir + "/share"

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'

    one_dof_arm_description_config = xacro.process_file(str(one_dof_arm_model_path))
    one_dof_arm_desc = one_dof_arm_description_config.toxml()

    robot_name = "upper_limb"
    #robot_name = ""
    if robot_name:
        namespace = "/" + robot_name
    else:
        namespace = ""

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        namespace=namespace,
    )

    joint_state_broadcaster_node = Node(
        package="controller_manager",
        executable="spawner.py",
        namespace=namespace,
        #arguments=["joint_state_broadcaster", "-c", namespace+"/controller_manager"],
        arguments=["upper_limb_joint_state_broadcaster", "-c", namespace+"/controller_manager"],
        output="screen",
    )

    joint_trajectory_controller_node = Node(
        package="controller_manager",
        executable="spawner.py",
        namespace=namespace,
        arguments=["upper_limb_joint_controller", "-c", namespace+"/controller_manager"],
        output="screen",
    )

    #  upper_limb_effort_controller_node = Node(
    #      package="controller_manager",
    #      executable="spawner.py",
    #      namespace=namespace,
    #      arguments=["upper_limb_effort_controller", "-c", namespace+"/controller_manager"],
    #      output="screen",
    #  )

    upper_limb_forward_command_controller_node = Node(
        package="controller_manager",
        executable="spawner.py",
        namespace=namespace,
        arguments=["upper_limb_forward_command_controller", "-c", namespace+"/controller_manager"],
        output="screen",
    )


    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        #Node(package='wearable_robot_description', executable='spawn_entity_v2.py', arguments=['upper_limb', one_dof_arm_desc, '0.8', '1.0', '0.9675'], output='screen'),
        #Node(package='wearable_robot_description', executable='spawn_entity_v2.py', arguments=['upper_limb', one_dof_arm_desc, '0.0', '0.0', '0.0'], output='screen'),
        #Node(package='wearable_robot_description', executable='spawn_entity.py', arguments=['one_dof_arm', one_dof_arm_desc], output='screen'),
        #Node(package='wearable_robot_description', executable='spawn_entity.py', arguments=['human', robot_desc], output='screen'),

        Node(package='gazebo_ros', 
             executable='spawn_entity.py',
             arguments=[
                 "-topic", namespace + "/robot_description",
                 "-entity", robot_name,
                 "-robot_namespace", namespace,
                 #  "-x", "1.18",
                 "-x", "1.200",
                 "-y", "1.015",
                 "-z", "1.0",
                 "-Y", "0.0",
                 "-unpause",
                 ],
             output='screen'),

        Node(
            package="robot_state_publisher",
            namespace=namespace,
            executable="robot_state_publisher",
            output="screen",
            remappings=[("/tf", "tf"), ("/tf_static", "tf_static")],
            parameters=[
                {"robot_description": one_dof_arm_desc}],
            ),

        #joint_state_publisher_node,
        joint_state_broadcaster_node,
        #joint_trajectory_controller_node,
        #upper_limb_effort_controller_node,
        upper_limb_forward_command_controller_node,
        launch.actions.TimerAction(
            actions=[launch.actions.LogInfo(msg="상지 웨어러블 디바이스 트윈 불러오기 완료")],
            period = 4.0
        ),
    ])

