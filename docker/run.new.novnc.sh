#!/bin/sh

ID=$@
NOVNC_PORT=$((8080 + $ID))
VNC_PORT=$((5900 + $ID))

docker run -it \
    --gpus all \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --rm \
    -p $NOVNC_PORT:6080 \
    -p $VNC_PORT:$VNC_PORT \
    --workdir="/root" \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :$ID && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:$VNC_PORT"
