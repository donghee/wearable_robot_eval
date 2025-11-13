#!/bin/sh

cd "$(dirname "$0")/.."

mkdir -p ./logs

pkill -f wearable_ui_frontend/tools/run.sh
pkill -f wearable_ui_backend/tools/run.sh

sh ./wearable_ui_frontend/tools/run.sh >> ./logs/frontend.log 2>&1 &
sh ./wearable_ui_backend/tools/run.sh >> ./logs/backend.log 2>&1 &

xhost +

code ./wearable_robot_mujoco
