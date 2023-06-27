#!/bin/bash
set -e

# setup ros2 environment
source "/opt/ros/$ROS_DISTRO/setup.bash" --
echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc

exec "$@"
