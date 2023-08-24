#!/bin/sh

xhost +local:root

# nvidia gpu
docker run -it \
    --gpus all \
    --privileged \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --rm \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --workdir="/root" \
    -p 6080:6080 \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "/bootstrap.sh && sudo chmod 777 -R /tmp/.X11-unix && /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :99 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:5999"

# no gpu
#docker run -it \
#    --privileged \
#    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
#    --rm \
#    --env="DISPLAY" \
#    --env="QT_X11_NO_MITSHM=1" \
#    --workdir="/root" \
#    ghcr.io/donghee/wearable_robot_eval:foxy \
#    bash
