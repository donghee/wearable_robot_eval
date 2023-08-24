# wearable_robot_eval

## Install

1. Build docker image

```
cd docker
docker build -t ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc . -f Dockerfile
```

2. Run docker container

ROS2 foxy in docker

```
cd docker
./run.sh
```

3. Run wearable robot evaluator in docker container

```
cd ~/ros2_ws/src/wearable_robot_eval
./run.eval.sh
```

TODO: Add evaluation screenshot

## Testing: 1 DOF ARM

Run wearable robot in Gazebo

1. Load human model

```
cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo human_only.launch.py
```

2. Load wearable robot model on human model

```
cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo eduexo_only.launch.py
```

3. Move wearable robot

```
cd ~/ros2_ws && python3 src/wearable_robot_eval/wearable_robot_description/scripts/1_dof_arm_gazebo_test.py -2.5
```

<img src="https://4249295727-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LmOTWbz2dgMNQsbqUOW%2Fuploads%2FmcNf8RBS3J8SGCYbRw81%2Fimage.png?alt=media&token=24b764e8-fdd2-4bc4-929d-607d819849a6"/>
