#!/bin/sh

# curl -o- https://raw.githubusercontent.com/donghee/wearable_robot_eval/2025/bin/install.sh | bash

cd ~
git clone -b 2025 --recursive https://github.com/donghee/wearable_robot_eval/
cd wearable_robot_eval
git pull
bash bin/setup.sh

