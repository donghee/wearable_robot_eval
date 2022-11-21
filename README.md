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
sudo apt install ros-foxy-gazebo-ros2-control ros-foxy-ros2-controllers ros-foxy-controller-manager ros-foxy-gazebo-ros2-control ros-foxy-ros2-controllers
```

Run robot in Gazebo

```
source /opt/ros/foxy/setup.bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone git@github.com:donghee/wearable_robot_eval.git
cd ~/ros2_ws/
colcon build
source ./install/setup.bash

ros2 launch wearable_robot_gazebo 1_dof_arm.launch.py
# or
ros2 launch wearable_robot_gazebo eduexo.launch.py
# or
ros2 launch wearable_robot_gazebo human.launch.py
```

<img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LmOTWbz2dgMNQsbqUOW%2Fuploads%2FGKPO7qbOmQkLJJRK81lr%2FPeek%202022-09-09%2023-48.gif?alt=media&token=ead262d0-0d96-4f38-9877-b5e175f84506"/>

---

Run wearable robot in Gazebo

1. load human model

```
cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo human_only.launch.py
```

2. load wearable robot model on human model

```
cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo eduexo_only.launch.py
```

3. move wearable robot

```
cd ~/ros2_ws && python3 src/wearable_robot_eval/wearable_robot_description/scripts/1_dof_arm_gazebo_test.py -2.5
```

<img src="https://4249295727-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LmOTWbz2dgMNQsbqUOW%2Fuploads%2FmcNf8RBS3J8SGCYbRw81%2Fimage.png?alt=media&token=24b764e8-fdd2-4bc4-929d-607d819849a6"/>
