#!/bin/bash
set -e

sudo /etc/init.d/nginx start

#source "/opt/ros/$ROS_DISTRO/setup.bash" --

if [ ! -d ~/ros2_ws/src ]; then
  mkdir -p ~/ros2_ws/src
  cd ~/ros2_ws/src
  git clone https://github.com/donghee/wearable_robot_eval.git
fi
cd ~/ros2_ws
rm -rf install bulid log

colcon build 
source ~/ros2_ws/install/setup.bash
