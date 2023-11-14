cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo human_45dof_wearing_upper_limb.launch.py

# test script
# device control
# cd ~/ros2_ws && source ./install/setup.bash && ros2 run wearable_robot_description upper_limb_gazebo_effort_test.py
# human control
# cd ~/ros2_ws && source ./install/setup.bash && ros2 run wearable_robot_description human_arm_gazebo_effort_test.py

# cd ~/ros2_ws && source ./install/setup.bash && ros2 launch wearable_robot_description evaluate_upper_limb.launch.py control_type:=square_wave
# cd ~/ros2_ws && source ./install/setup.bash && ros2 launch wearable_robot_description evaluate_upper_limb.launch.py control_type:=square_wave_failed
# cd ~/ros2_ws && source ./install/setup.bash && ros2 launch wearable_robot_description evaluate_upper_limb.launch.py control_type:=zero

