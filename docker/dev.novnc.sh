#!/bin/sh

ID=9
NOVNC_PORT=$((8080 + $ID))
VNC_PORT=$((5900 + $ID))

docker run -it \
    --gpus all \
    --volume="/tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw" \
    --volume="$HOME/ros2_ws:/root/dev_ws:rw" \
    --volume="$HOME/.ssh:/root/.ssh:ro" \
    --rm \
    -p 80:6080 \
    -p $NOVNC_PORT:6080 \
    -p $VNC_PORT:$VNC_PORT \
    --workdir="/root" \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "/opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :$ID && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:$VNC_PORT"
    #bash -c "/opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ --token-plugin=TokenFile --token-source=/root/.vnc/websockify-token.cfg 6080"
