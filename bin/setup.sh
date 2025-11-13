#!/bin/sh

cd "$(dirname "$0")/.."

# Install docker if not installed
if ! [ -x "$(command -v docker)" ]; then
    echo 'Docker is not installed. Installing Docker...'
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    sudo usermod -aG docker $USER
else
    echo 'Docker is already installed.'
fi

# Create Index.dat to prepare frontend 
touch Index.dat
mkdir -p Patient

sh ./wearable_ui_frontend/tools/setup.sh
sh ./wearable_ui_backend/tools/setup.sh
sh ./wearable_robot_mujoco/docker/setup.sh
sh ./wearable_vscode_extention/tools/setup.sh

# Install latest VSCode
wget "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" -O vscode.deb
sudo dpkg -i vscode.deb
rm vscode.deb

code --install-extension ./wearable_vscode_extention/wearable-vscode-extension-0.0.1.vsix
