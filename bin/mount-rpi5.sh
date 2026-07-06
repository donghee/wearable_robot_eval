#!/bin/bash

sudo umount ~/wearable_robot_eval/wearable_robot_upper_limb
mkdir -p ~/wearable_robot_eval/wearable_robot_upper_limb
#sshfs donghee@100.90.168.18:dynamixel_ws/src/wearable_robot_upper_limb/ ~/wearable_robot_eval/wearable_robot_upper_limb
#sshfs donghee@192.168.88.26:dynamixel_ws/src/wearable_robot_upper_limb/ ~/wearable_robot_eval/wearable_robot_upper_limb
sshfs donghee@172.30.1.41:dynamixel_ws/src/wearable_robot_upper_limb/ ~/wearable_robot_eval/wearable_robot_upper_limb

df
