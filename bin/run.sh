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

echo "Waiting for services to start..."
sleep 10
echo "Opening Wearable UI Frontend in browser..."
open http://localhost:5005
