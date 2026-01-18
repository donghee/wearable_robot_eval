#!/bin/bash

cd "$(dirname "$0")/.."

# tar current directory excluding .venv node_modules and __pycache__
tar --exclude='.venv' --exclude='node_modules' --exclude='__pycache__' -czf ../wearable_robot_eval_$(date +%Y%m%d_%H%M%S).tar.gz .
