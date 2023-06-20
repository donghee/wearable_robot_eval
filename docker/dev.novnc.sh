#!/bin/sh

docker run -it \
    --gpus all \
    -e DISPLAY=:1 \
    --volume="/tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw" \
    --volume="$HOME/ros2_ws:/root/dev_ws:rw" \
    --volume="$HOME/.ssh:/root/.ssh:ro" \
    --rm \
    -p 80:6080 \
    -p 5901:5901 \
    --workdir="/root" \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "touch ~/.Xauthority;xauth generate :0 . trusted;/opt/TurboVNC/bin/vncserver -wm xfce -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:5901"
    #bash -c "touch ~/.Xauthority;xauth generate :0 . trusted;/opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:5901"
    #bash -c "TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:5901"
    #bash -c "TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ --token-plugin=TokenFile --token-source=/root/.vnc/websockify-token.cfg 6080"
    #bash -c "/root/ros2_ws/src/wearable_robot_eval/docker/novnc.sh"
