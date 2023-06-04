#!/bin/sh

TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 && /opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ --token-plugin=TokenFile --token-source=/root/.vnc/websockify-token.cfg 6080
