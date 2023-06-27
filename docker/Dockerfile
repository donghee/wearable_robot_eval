FROM osrf/ros:foxy-desktop
LABEL maintainer="Donghee Park <dongheepark@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    sudo \
    openssh-client \
    git \
    openssl \
    locales \
    && rm -rf /var/lib/apt/lists/*

# configure timezone
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo "Asia/Seoul" > /etc/timezone
 
# configure locale
RUN export LANGUAGE=ko_KR.UTF-8; export LANG=ko_KR.UTF-8; export LC_ALL=ko_KR.UTF-8; locale-gen ko_KR.UTF-8; DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
RUN echo "LANG=ko_KR.UTF-8" > /etc/default/locale
RUN echo "LANGUAGE=ko_KR.UTF-8" >> /etc/default/locale
RUN echo "LC_ALL=ko_KR.UTF-8" >> /etc/default/locale

ENV LANG ko_KR.UTF-8 
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

RUN apt-get update && apt-get install --no-install-recommends -y \
  ros-foxy-gazebo-dev \
  ros-foxy-gazebo-plugins \
  ros-foxy-gazebo-msgs \
  ros-foxy-gazebo-ros-pkgs \
  ros-foxy-gazebo-ros \
  ros-foxy-ros-core \
  ros-foxy-geometry2 \
  ros-foxy-joint-state-publisher-gui \
  ros-foxy-xacro \
  ros-foxy-gazebo-ros2-control \
  ros-foxy-ros2-controllers \
  ros-foxy-controller-manager \
  ros-foxy-gazebo-ros2-control \
  ros-foxy-ros2-controllers \
  tilix \
  tmux \
  vim

# FIXME: provide fix for theese root-need
RUN apt-get update && apt-get install --no-install-recommends -y \
    apt-rdepends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $HOME

COPY ./ros_entrypoint.sh /
COPY ./bootstrap.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]
