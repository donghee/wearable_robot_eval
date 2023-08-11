#!/bin/bash

cd ~/ros2_ws 
colcon build
cd ~/ros2_ws/src/wearable_robot_eval
. ~/ros2_ws/install/setup.bash

# Run Simulation and Wearability, Interactivity
clear
python3 run.eval.py

# Usability
clear
pushd ./wearable_robot_evaluation/usability
./act-r.sh 10
popd

echo "Finish"
