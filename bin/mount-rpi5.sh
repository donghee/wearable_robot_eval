#!/bin/bash

sudo umount ~/wearable_robot_eval/wearable_robot_upper_limb
mkdir -p ~/wearable_robot_eval/wearable_robot_upper_limb
sshfs donghee@100.90.168.18:dynamixel_ws/src/wearable_robot_upper_limb/ ~/wearable_robot_eval/wearable_robot_upper_limb

df
