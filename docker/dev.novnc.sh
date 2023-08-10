#!/bin/sh

sudo chmod -R 777 /tmp/.X11-unix

ID=9
VNC_PORT=$((5900 + $ID))

#docker run -it \
docker run \
    --gpus all \
    --privileged  \
    --volume="/tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw" \
    --volume="$HOME/ros2_ws:$HOME/ros2_ws:rw" \
    --volume="$HOME/src:$HOME/src:rw" \
    --volume="$HOME/.ssh:$HOME/.ssh:ro" \
    --rm \
    -p 80:6080 \
    -p $VNC_PORT:$VNC_PORT \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc_user \
    bash -c "sudo chmod 777 -R /tmp/.X11-unix && /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :$ID && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:$VNC_PORT"
    
#   --workdir="/root" \
