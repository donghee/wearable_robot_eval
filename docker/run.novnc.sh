#!/bin/sh

usage()
{
  echo "Usage: ./`basename $0` 1~8"
  exit $1
}

if [ $# -eq 0 ]
then
  usage 0
fi


ID=$@
NOVNC_PORT=$((8080 + $ID))
VNC_PORT=$((5900 + $ID))

docker run -it \
    --gpus all \
    --privileged \
    --volume="/tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw" \
    --rm \
    -p $NOVNC_PORT:6080 \
    -p $VNC_PORT:$VNC_PORT \
    --workdir="/root" \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc \
    bash -c "/bootstrap.sh && /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :$ID && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:$VNC_PORT"
