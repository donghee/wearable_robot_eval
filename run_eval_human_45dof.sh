#!/bin/bash

cd ~/ros2_ws 
colcon build --symlink-install
cd ~/ros2_ws/src/wearable_robot_eval
. ~/ros2_ws/install/setup.bash

# Run Simulation and Wearability, Interactivity, Usability Evaluation
clear
python3 run_eval_human_45dof.py
