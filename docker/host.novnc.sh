#!/bin/sh

ID=9
NOVNC_PORT=$((8080 + $ID))
VNC_PORT=$((5900 + $ID))

#docker run -it \
docker run \
    --network host \
    --gpus all \
    --privileged  \
    --volume="/tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw" \
    --volume="$HOME/.ssh:/root/.ssh:ro" \
    --rm \
    --workdir="/root" \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "/opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :$ID && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:$VNC_PORT"
