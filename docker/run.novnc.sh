#!/bin/sh

docker run -it \
    --gpus all \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --rm \
    -p 80:6080 \
    --workdir="/root" \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:5901"
    #bash -c "TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ --token-plugin=TokenFile --token-source=/root/.vnc/websockify-token.cfg 6080"
    #bash -c "/root/ros2_ws/src/wearable_robot_eval/docker/novnc.sh"
