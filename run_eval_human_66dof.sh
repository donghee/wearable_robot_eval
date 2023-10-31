#!/bin/bash

cd ~/ros2_ws 
colcon build
cd ~/ros2_ws/src/wearable_robot_eval
. ~/ros2_ws/install/setup.bash

# Run Simulation and Wearability, Interactivity, Usability Evaluation using human_66dof.urdf with right arm's eduexo
clear
python3 run_eval_human_66dof.py
