cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo upper_limb.launch.py

# test script
#cd ~/ros2_ws && source ./install/setup.bash && ros2 run wearable_robot_description upper_limb_gazebo_effort_test.py