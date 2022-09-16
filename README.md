# wearable_robot_eval

## Install

ROS2 foxy in Docker

```
xhost +local:root

docker run -it \
    --privileged -v /dev/bus/usb:/dev/bus/usb \
    --user $(id -u) \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --workdir="/home/$USER" \
    --volume="/home/$USER:/home/$USER" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    osrf/ros:foxy-desktop \
    bash
```

Required ROS packages

```
sudo apt install ros-foxy-gazebo-dev ros-foxy-gazebo-plugins ros-foxy-gazebo-msgs ros-foxy-gazebo-ros-pkgs ros-foxy-gazebo-ros ros-foxy-ros-core ros-foxy-geometry2
sudo apt install ros-foxy-joint-state-publisher-gui ros-foxy-xacro
sudo apt install ros-foxy-gazebo-ros2-control ros-foxy-ros2-controllers ros-foxy-controller-manager ros-foxy-gazebo-ros2-control ros-ros-foxy-ros2-controllers
```

Run robot in Gazebo
```
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone git@github.com:donghee/wearable_robot_eval.git
cd ~/ros2_ws/
colcon build
source ./install/setup.bash

ros2 launch wearable_robot_gazebo 1_dof_arm.launch.py
# or 
ros2 launch wearable_robot_gazebo eduexo.launch.py
```

<img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LmOTWbz2dgMNQsbqUOW%2Fuploads%2FGKPO7qbOmQkLJJRK81lr%2FPeek%202022-09-09%2023-48.gif?alt=media&token=ead262d0-0d96-4f38-9877-b5e175f84506"/>
