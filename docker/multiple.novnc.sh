#!/bin/sh

TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :1 
TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :2
TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :3 
TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :4 
TVNC_VGL=1 /opt/TurboVNC/bin/vncserver -wm LXDE -SecurityTypes None :5 

cat <<EOL >> /root/.vnc/websockify-token.cfg
p1: 127.0.0.1:5901
p2: 127.0.0.1:5902
p3: 127.0.0.1:5903
p4: 127.0.0.1:5904
p5: 127.0.0.1:5905
EOL

/opt/noVNC/utils/websockify/run --verbose --web=/opt/noVNC/ --token-plugin=TokenFile --token-source=/root/.vnc/websockify-token.cfg 6080
