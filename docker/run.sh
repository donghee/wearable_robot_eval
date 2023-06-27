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
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "/bootstrap.sh && bash"

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
