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
import launch.events
import launch.substitutions
from launch.actions import ExecuteProcess

import xacro

def generate_launch_description():
    pkg_wearable_robot_path = get_package_share_path('wearable_robot_description')
    default_model_path = pkg_wearable_robot_path / 'urdf/human_66dof.xacro'
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

    human_description_config = xacro.process_file(str(default_model_path))
    human_desc = human_description_config.toxml()

    robot_name = "human"
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
        arguments=["joint_state_broadcaster", "-c", namespace+"/controller_manager"],
        output="screen",
    )

    joint_trajectory_controller_node = Node(
        package="controller_manager",
        executable="spawner.py",
        namespace=namespace,
        arguments=["joint_trajectory_controller", "-c", namespace+"/controller_manager"],
        output="screen",
    )

    effort_controller_node = Node(
        package="controller_manager",
        executable="spawner.py",
        namespace=namespace,
        arguments=["effort_controller", "-c", namespace+"/controller_manager"],
        output="screen",
    )


    load_joint_state_broadcaster = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "start", # use start when ROS_DISTRO is foxy
            "joint_state_broadcaster",
            "-c",
            namespace + "/controller_manager",
        ],
        output="screen",
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "start", # use start when ROS_DISTRO is foxy
            "joint_trajectory_controller",
            "-c",
            namespace + "/controller_manager",
        ],
        output="screen",
    )

    # https://robotics.snowcron.com/robotics_ros2/multi_bot_03_launch.htm
    ld = LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        #Node(
        #    package='wearable_robot_description', 
        #    executable='spawn_entity.py', 
        #    #arguments=['human', robot_desc, 'human'], 
        #    arguments=['human', robot_desc, ''], 
        #    output='screen'),

        Node(package='gazebo_ros', 
             executable='spawn_entity.py',
             arguments=[
                 "-topic", namespace + "/robot_description",
                 "-entity", robot_name,
                 "-robot_namespace", namespace,
                 "-x", "0.0",
                 "-y", "0.0",
                 "-z", "0.0",
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
                {"robot_description": human_desc}],
            ),
        #joint_state_publisher_node,

        joint_state_broadcaster_node,
        #joint_trajectory_controller_node,
        effort_controller_node,

        #load_joint_state_broadcaster,
        #load_joint_trajectory_controller,
        launch.actions.TimerAction(
            actions=[launch.actions.LogInfo(msg="휴먼 트윈 생성 완료")],
            period = 4.0
        )
    ])

    ld.add_action(launch.actions.RegisterEventHandler(launch.event_handlers.OnShutdown(
        on_shutdown=[launch.actions.LogInfo(msg=[
            '동작 수행에 따른 데이터 저장 완료\n                      ---------------------------------',
            launch.substitutions.LocalSubstitution('event.reason'),
        ])],
    )))

    return ld
