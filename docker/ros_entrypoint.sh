#!/bin/bash
set -e

# setup ros2 environment
source "/opt/ros/$ROS_DISTRO/setup.bash" --

mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/donghee/wearable_robot_eval.git
cd ~/ros2_ws
colcon build 
source ~/ros2_ws/install/setup.bash

exec "$@"
