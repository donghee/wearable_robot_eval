xhost +local:root

docker run -it \
    --privileged -v /dev/bus/usb:/dev/bus/usb \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --workdir="/root" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    ghcr.io/donghee/wearable_robot_eval:foxy \
    bash
