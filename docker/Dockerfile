FROM nvidia/opengl:1.2-glvnd-runtime-ubuntu20.04
LABEL maintainer="Donghee Park <dongheepark@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    sudo \
    openssh-client \
    git \
    openssl \
    locales \
    software-properties-common \
    dirmngr \
    gpg-agent \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo "Asia/Seoul" > /etc/timezone
 
# Configure locale
RUN export LANGUAGE=ko_KR.UTF-8; export LANG=ko_KR.UTF-8; export LC_ALL=ko_KR.UTF-8; locale-gen ko_KR.UTF-8; DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
RUN echo "LANG=ko_KR.UTF-8" > /etc/default/locale
RUN echo "LANGUAGE=ko_KR.UTF-8" >> /etc/default/locale
RUN echo "LC_ALL=ko_KR.UTF-8" >> /etc/default/locale

ENV LANG ko_KR.UTF-8 
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# nvidia opengl
RUN dpkg --add-architecture i386 \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
        libxau6 libxau6:i386 \
        libxdmcp6 libxdmcp6:i386 \
        libxcb1 libxcb1:i386 \
        libxext6 libxext6:i386 \
        libx11-6 libx11-6:i386 && \
    rm -rf /var/lib/apt/lists/*

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
        ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
        ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics,compat32,utility

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

# Required for non-glvnd setups.
ENV LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu:/usr/lib/i386-linux-gnu${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}:/usr/local/nvidia/lib:/usr/local/nvidia/lib64

#####
# Copied from
# https://gitlab.com/nvidia/container-images/opengl/blob/ubuntu20.04/glvnd/devel/Dockerfile
# and removed :i386 packages (not found)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        pkg-config \
        libglvnd-dev libglvnd-dev:i386 \
        libgl1-mesa-dev libgl1-mesa-dev:i386 \
        libegl1-mesa-dev libegl1-mesa-dev:i386 \
        libgles2-mesa-dev libgles2-mesa-dev:i386 && \
    rm -rf /var/lib/apt/lists/*

# ROS
ENV ROS_DISTRO=foxy
ENV ROS_ROOT=/opt/ros/${ROS_DISTRO}

#RUN apt-get update && apt-get install -y curl gnupg2 lsb-release && \
#  curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -i
#RUN sh -c 'echo "deb [arch=amd64,arm64] http://packages.ros.org/ros2/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros2-latest.list'
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
RUN echo "deb http://packages.ros.org/ros2/ubuntu focal main" > /etc/apt/sources.list.d/ros2-latest.list

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python3-pip \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-rosdep \
    python3-vcstool \
   && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install --no-install-recommends -y \
    ros-${ROS_DISTRO}-desktop \
    python3-argcomplete \
    ros-dev-tools \ 
   && rm -rf /var/lib/apt/lists/*

# Install python packages
RUN pip3 install -U \
    argcomplete \
    flake8 \
    flake8-blind-except \
    flake8-builtins \
    flake8-class-newline \
    flake8-comprehensions \
    flake8-deprecated \
    flake8-docstrings \
    flake8-import-order \
    flake8-quotes \
    pytest-repeat \
    pytest-rerunfailures
# This is a workaround for pytest not found causing builds to fail
# Following RUN statements tests for regression of https://github.com/ros2/ros2/issues/722
RUN pip3 freeze | grep pytest \
    && python3 -m pytest --version

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

# setup colcon mixin and metadata
RUN colcon mixin add default \
      https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml && \
    colcon mixin update && \
    colcon metadata add default \
      https://raw.githubusercontent.com/colcon/colcon-metadata-repository/master/index.yaml && \
    colcon metadata update

RUN apt-get update && apt-get install --no-install-recommends -y \
  ros-${ROS_DISTRO}-gazebo-dev \
  ros-${ROS_DISTRO}-gazebo-plugins \
  ros-${ROS_DISTRO}-gazebo-msgs \
  ros-${ROS_DISTRO}-gazebo-ros-pkgs \
  ros-${ROS_DISTRO}-gazebo-ros \
  ros-${ROS_DISTRO}-ros-core \
  ros-${ROS_DISTRO}-geometry2 \
  ros-${ROS_DISTRO}-joint-state-publisher-gui \
  ros-${ROS_DISTRO}-xacro \
  ros-${ROS_DISTRO}-gazebo-ros2-control \
  ros-${ROS_DISTRO}-ros2-controllers \
  ros-${ROS_DISTRO}-controller-manager \
  ros-${ROS_DISTRO}-gazebo-ros2-control \
  ros-${ROS_DISTRO}-ros2-controllers \
  tmux \
  vim

# FIXME: provide fix for these root-need
RUN apt-get update && apt-get install --no-install-recommends -y \
    apt-rdepends \
    && rm -rf /var/lib/apt/lists/*

# turbovnc
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    lxde-core \
    terminator \
    tilix \
    tmuxinator \
    mesa-utils \
    libglu1 \
    libsm6 \
    libxv1 \
    libxtst6 \
    libegl1-mesa \
    x11-xkb-utils \
    xauth \
    python3-numpy \
    xfonts-base \
    xkb-data \
    lxde \
    xfce4 \
    xfce4-power-manager \
    nginx \ 
    htop \
    gedit \
    firefox \
    fonts-noto-cjk \
    arc-theme \
    papirus-icon-theme \
    uim uim-xim uim-byeoru uim-gtk3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

ARG TURBOVNC_VERSION=3.0.3
ARG VIRTUALGL_VERSION=3.1
ARG LIBJPEG_VERSION=2.1.5.1

RUN cd /tmp && \
    curl -O https://nchc.dl.sourceforge.net/project/turbovnc/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb
RUN cd /tmp && \
    curl -L -O https://nchc.dl.sourceforge.net/project/libjpeg-turbo/${LIBJPEG_VERSION}/libjpeg-turbo-official_${LIBJPEG_VERSION}_amd64.deb
RUN cd /tmp && \
    curl -O https://nchc.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb
#RUN cd /tmp && \
#    curl -O https://master.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl32_${VIRTUALGL_VERSION}_amd64.deb?viasf=1

RUN cd /tmp && \
    dpkg -i *.deb && \
    rm -f /tmp/*.deb
#    rm -f /tmp/*.deb && \
#    sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver

ENV PATH ${PATH}:/opt/VirtualGL/bin:/opt/TurboVNC/bin

# noVNC
WORKDIR /opt/
RUN git clone https://github.com/novnc/noVNC.git
WORKDIR /opt/noVNC/utils/
RUN git clone https://github.com/novnc/websockify
#RUN mkdir -p $HOME/.vnc
#COPY files/websockify-token.cfg $HOME/.vnc/

COPY files/xorg.conf /etc/X11/xorg.conf

RUN mv /etc/xdg/autostart/light-locker.desktop /etc/xdg/autostart/light-locker.desktop_bak
RUN mv /etc/xdg/autostart/xfce4-power-manager.desktop /etc/xdg/autostart/xfce4-power-manager.desktop_bak
RUN mv /usr/bin/lxpolkit /usr/bin/lxpolkit_bak
 
# wearable robot evaluation
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk libbz2-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN pip3 install -U \
    pandas scipy urdf_parser_py flask

RUN cd /tmp && \
    curl -L -O http://prdownloads.sourceforge.net/sbcl/sbcl-2.0.9-x86-64-linux-binary.tar.bz2 && \
    tar -xf sbcl-2.0.9-x86-64-linux-binary.tar.bz2 && rm sbcl-2.0.9-x86-64-linux-binary.tar.bz2 && \
    cd sbcl-2.0.9-x86-64-linux && sudo sh install.sh && cd .. && rm -r sbcl-2.0.9-x86-64-linux && \
    wget https://beta.quicklisp.org/quicklisp.lisp && sbcl --quit --load quicklisp.lisp --eval '(quicklisp-quickstart:install :path "quicklisp")' && rm quicklisp.lisp

# Add user to share files and folder without root permissions
ARG UID=1000
ARG GID=1000
ARG USER=root
ARG HOME=/root

RUN if [ "$USER" != "root" ]; then \
 addgroup --gid $GID $USER && adduser --disabled-password --gecos '' --uid $UID --gid $GID $USER \
 && echo "vglusers:x:1001:${USER}" >> /etc/group \
 && echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
fi

WORKDIR $HOME
USER $USER

# Use --build-arg CACHEBUST=$(date +%s) to force this layer to re-run
ARG CACHEBUST=1

# desktop
RUN mkdir -p $HOME/Desktop
#COPY files/firefox.desktop_applications /usr/share/applications/firefox.desktop
COPY files/terminator.desktop $HOME/Desktop
RUN mkdir -p $HOME/.config/terminator
COPY files/firefox.desktop $HOME/Desktop
COPY files/htop.desktop $HOME/Desktop
COPY files/gedit.desktop $HOME/Desktop
COPY files/background.png /tmp
RUN sudo perl -pi -e 's/^Exec=terminator$/Exec=terminator -e "vglrun bash"/g' /usr/share/applications/terminator.desktop

# xim
ENV GTK_IM_MODULE uim
ENV QT_IM_MODULE uim
ENV XMODIFIERS @im=uim
RUN mkdir -p $HOME/.config/lxsession/LXDE
COPY files/autostart $HOME/.config/lxsession/LXDE

# GTK 2 and 3 settings for icons and style, wallpaper
RUN echo '\n\
gtk-theme-name="Arc-Darker"\n\
gtk-icon-theme-name="Papirus"\n\
' > $HOME/.config/.gtkrc-2.0 && \
\
mkdir -p $HOME/.config/gtk-3.0 && \
echo '\n\
[Settings]\n\
gtk-theme-name="Arc-Darker"\n\
gtk-icon-theme-name="Papirus"\n\
' > $HOME/.config/gtk-3.0/settings.ini && \
\
mkdir -p $HOME/.config/pcmanfm/LXDE && \
echo '\n\
[*]\n\
wallpaper_mode=stretch\n\
wallpaper_common=1\n\
wallpaper=/tmp/background.png\n\
' > $HOME/.config/pcmanfm/LXDE/desktop-items-0.conf && \
\
mkdir -p $HOME/.config/libfm && \
echo '\n\
[config]\n\
quick_exec=1\n\
terminal=lxterminal\n\
' > $HOME/.config/libfm/libfm.conf && \
\
mkdir -p $HOME/.config/openbox/ && \
echo '<?xml version="1.0" encoding="UTF-8"?>\n\
<theme>\n\
  <name>Arc-Darker</name>\n\
</theme>\n\
' > $HOME/.config/openbox/lxde-rc.xml && \
\
mkdir -p $HOME/.config/lxsession/LXDE/ && \
echo '[Session]\n\
window_manager=openbox-lxde\n\
[GTK]\n\
sNet/ThemeName=Arc-Darker\n\
sNet/IconThemeName=Papirus\n\
' > $HOME/.config/lxsession/LXDE/desktop.conf 
#' > $HOME/.config/lxsession/LXDE/desktop.conf && \
#mkdir -p /etc/skel/.config/ && \
#echo '[Added Associations]\n\
#text/plain=mousepad.desktop;\n\
#' > /etc/skel/.config/mimeapps.list

# /etc/xdg/openbox/rc.xml Clearlooks -> Arc-Darker
RUN sudo sed -i "s/Clearlooks/Arc-Darker/g" /etc/xdg/openbox/rc.xml
RUN mkdir -p $HOME/.config/lxpanel/LXDE/panels/
COPY files/panel $HOME/.config/lxpanel/LXDE/panels/

# nginx
COPY files/nginx.conf /etc/nginx/sites-available/default

RUN sudo chown -R $USER:$USER $HOME

COPY ./bootstrap.sh /
COPY ./ros_entrypoint.sh /

# nginx
COPY files/nginx.conf /etc/nginx/sites-enabled/default

ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["bash"]
