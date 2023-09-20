#!/bin/sh
#
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
NOVNC_PORT=$((6080 + $ID))
VNC_PORT=$((5900 + $ID))
HTTP_PORT=80

docker run -it \
    --gpus all \
    --privileged  \
    --volume="/tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw" \
    --volume="$HOME/ros2_ws:$HOME/ros2_ws:rw" \
    --volume="$HOME/src:$HOME/src:rw" \
    --volume="$HOME/.ssh:$HOME/.ssh:ro" \
    --workdir="${HOME}" \
    --user="$(id -u):$(id -g)" \
    --rm \
    -p 80:80 \
    -p $NOVNC_PORT:6080 \
    -p $VNC_PORT:$VNC_PORT \
    ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc_user_$USER \
    bash -c "/bootstrap.sh && sudo chmod 777 -R /tmp/.X11-unix && /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :$ID && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ 6080 127.0.0.1:$VNC_PORT"
    
#    -p $HTTP_PORT:80 \
#    --user="$(id -u):$(stat -c %g /dev/nvidia0)"
