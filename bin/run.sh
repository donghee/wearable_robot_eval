#!/bin/sh

cd "$(dirname "$0")/.."

mkdir -p ./logs

pkill -f wearable_ui_frontend/tools/run.sh
pkill -f wearable_ui_backend/tools/run.sh

echo "Starting Wearable UI Frontend..."
sh ./wearable_ui_frontend/tools/run.sh >> ./logs/frontend.log 2>&1 &

echo "Starting Wearable UI Backend..."
sh ./wearable_ui_backend/tools/run.sh >> ./logs/backend.log 2>&1 &

xhost +

echo "Starting VSCODE..."
code ./wearable_robot_mujoco

sleep 2
DISPLAY_SIZE=$(xdpyinfo | grep 'dimensions:' | awk '{print $2}')
WIDTH=$(echo $DISPLAY_SIZE | cut -d'x' -f1)
HEIGHT=$(echo $DISPLAY_SIZE | cut -d'x' -f2)
WIDTH_TWO_THIRDS=$((WIDTH * 2 / 3))
WIDTH_ONE_THIRD=$((WIDTH / 3))
wmctrl -r "Visual Studio Code" -e "0,0,0,$WIDTH_TWO_THIRDS,$HEIGHT"

echo "Waiting for services to start..."
sleep 10
#echo "Opening Wearable UI Frontend in browser..."
#open http://localhost:5005
