#!/bin/sh

set -e

command_exists() {
  command -v "$@" >/dev/null 2>&1
}

user_can_sudo() {
  command_exists sudo || return 1
  ! LANG= sudo -n -v 2>&1 | grep -q "may not run sudo"
}

RUN=$(user_can_sudo && echo "sudo" || echo "command")

install_tools() {
  $RUN apt-get install --no-install-recommends -y git curl wget ssh tmux tmuxinator unzip vim
}

install_xtools() {
  $RUN apt-get install -y tilix lxterminal terminator
}

install_zsh() {
  $RUN apt-get install --no-install-recommends -y zsh
  $RUN chsh -s /bin/zsh
  curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh -s -- -y
}

install_nvim() {
  $RUN apt-get install --no-install-recommends -y software-properties-common gnupg
  $RUN add-apt-repository ppa:neovim-ppa/unstable -y
  $RUN apt-get update
  $RUN apt-get install --no-install-recommends -y neovim luajit
  $RUN update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 60
  $RUN update-alternatives --install /usr/bin/vim vim /usr/bin/nvim 60
  $RUN update-alternatives --install /usr/bin/editor editor /usr/bin/nvim 60
  #git clone --depth 1 https://github.com/wbthomason/packer.nvim $HOME/.local/share/nvim/site/pack/packer/start/packer.nvim && \
  nvim --headless -c 'q!'
  #nvim --headless -c 'sleep 5' -c 'autocmd User PackerComplete quitall' -c 'PackerSync'
  #nvim --headless -c 'sleep 5' -c 'Copilot setup'

  # copy nvim config
  ln -sf ~/src/github.com/donghee/dotfiles/.config/nvim ~/.config/nvim
  cp ~/src/github.com/donghee/dotfiles/.profile ~/.profile
  cp ~/src/github.com/donghee/dotfiles/docker/files/.gitconfig ~/
}

install_emacs() {
  $RUN apt-get install --no-install-recommends -y software-properties-common gnupg
  $RUN add-apt-repository ppa:ubuntu-elisp/ppa -y
  $RUN apt-get update
  $RUN apt-get install --no-install-recommends -y emacs-snapshot
}

install_node() {
  NODE_VERSION=$1

  # nvm
  echo 'export NVM_DIR="$HOME/.nvm"'                                       >> "$HOME/.bashrc"
  echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm' >> "$HOME/.bashrc"
  echo '[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion" # This loads nvm bash_completion' >> "$HOME/.bashrc"

  # nodejs and tools
  curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
  bash -c 'source $HOME/.nvm/nvm.sh   && \
      nvm install node            && \
      nvm use default'
}

install_rust() {
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  export PATH=$PATH:$HOME/.cargo/bin/
}

install_cpp() {
  $RUN apt-get install --no-install-recommends -y cmake build-essential entr
}

install_python() {
  PYTHON_VERSION=$1
  $RUN apt-get install --no-install-recommends -y python3-pip build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev
  curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
  curl -sSL https://install.python-poetry.org | python3 -
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$HOME/.local/bin:$PATH"

  echo 'export PYENV_ROOT="$HOME/.pyenv"'  >> "$HOME/.bashrc"
  echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"'  >> "$HOME/.bashrc"
  echo 'eval "$(pyenv init -)"'  >> "$HOME/.bashrc"
  echo 'eval "$(pyenv virtualenv-init -)"'  >> "$HOME/.bashrc"

  pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    pyenv rehash
}

install_scripts() {
  mkdir -p $HOME/.local/bin && export PATH=$PATH:$HOME/.local/bin/
}

install_yadm() {
  # TODO: Add support for non-root user, else loop is already working
  mkdir -p $HOME/.local/bin && export PATH=$PATH:$HOME/.local/bin/
  curl -fLo $HOME/.local/bin/yadm https://github.com/TheLocehiliosan/yadm/raw/master/yadm && chmod a+x $HOME/.local/bin/yadm

  cd $HOME
  yadm checkout ~/.profile
  yadm checkout ~/.gitconfig
  yadm checkout ~/.zshrc
}

install_fonts() {
  mkdir -p ~/.local/share/fonts && \
    wget -q https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.2/FiraCode.zip -O FiraCode.zip && \
    unzip -o -q FiraCode.zip -d  ~/.local/share/fonts && \
    rm FiraCode.zip 

  fc-cache ~/.local/share/fonts
}

install_lxde() {
  $RUN apt-get install --no-install-recommends -y \
      lxde-core \
      lxde \
      light-locker \
      xfce4-power-manager \
      fonts-noto-cjk \
      arc-theme \
      papirus-icon-theme \
      uim uim-xim uim-byeoru uim-gtk3
 
  $RUN mv /etc/xdg/autostart/light-locker.desktop /etc/xdg/autostart/light-locker.desktop_bak
  $RUN mv /etc/xdg/autostart/xfce4-power-manager.desktop /etc/xdg/autostart/xfce4-power-manager.desktop_bak
  $RUN mv /usr/bin/lxpolkit /usr/bin/lxpolkit_bak

  # desktop
  mkdir -p $HOME/Desktop

  # xim
  $RUN echo 'GTK_IM_MODULE=uim
QT_IM_MODULE=uim
XMODIFIERS=@im=uim' | sudo tee -a /etc/environment.d/10-xim.conf > /dev/null
#' | sudo tee -a /etc/profile.d/02-xim.sh > /dev/null

  mkdir -p $HOME/.config/lxsession/LXDE
  $RUN echo '@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@xscreensaver -no-splash
@uim-xim
@uim-toolbar-gtk3-systray
' > $HOME/.config/lxsession/LXDE/autostart

  # GTK 2 and 3 settings for icons and style, wallpaper
  $RUN echo 'gtk-theme-name="Arc-Darker"
gtk-icon-theme-name="Papirus"
' > $HOME/.config/.gtkrc-2.0 && \
  \
  mkdir -p $HOME/.config/gtk-3.0 && \
  echo '[Settings]
gtk-theme-name="Arc-Darker"
gtk-icon-theme-name="Papirus"
' > $HOME/.config/gtk-3.0/settings.ini && \
  \
  mkdir -p $HOME/.config/pcmanfm/LXDE && \
  echo '[*]
wallpaper_mode=stretch
wallpaper_common=1
wallpaper=/tmp/background.png
' > $HOME/.config/pcmanfm/LXDE/desktop-items-0.conf && \
  \
  mkdir -p $HOME/.config/libfm && \
  echo '[config]
quick_exec=1
terminal=lxterminal
' > $HOME/.config/libfm/libfm.conf && \
  \
  mkdir -p $HOME/.config/openbox/ && \
  echo '<?xml version="1.0" encoding="UTF-8"?>
<theme>
  <name>Arc-Darker</name>
</theme>
' > $HOME/.config/openbox/lxde-rc.xml && \
  \
  mkdir -p $HOME/.config/lxsession/LXDE/ && \
  echo '[Session]
window_manager=openbox-lxde
[GTK]
sNet/ThemeName=Arc-Darker
sNet/IconThemeName=Papirus
' > $HOME/.config/lxsession/LXDE/desktop.conf && \

  # Ubuntu 22.04's arc-theme do not support openbox
  $RUN curl -L -O https://github.com/arc-design/arc-theme/archive/refs/tags/20190917.zip && \
  unzip -o 20190917.zip && \
  mkdir -p ~/.themes && \
  mv ./arc-theme-20190917/common/openbox/* ~/.themes && \
  rm -r 20190917.zip arc-theme-20190917

  # /etc/xdg/openbox/rc.xml Clearlooks -> Arc-Darker
  $RUN sudo sed -i "s/Clearlooks/Arc-Darker/g" /etc/xdg/openbox/rc.xml
  mkdir -p $HOME/.config/lxpanel/LXDE/panels/ && \
  echo 'Global {
  edge=top
  allign=left
  margin=0
  widthtype=percent
  width=100
  height=36
  transparent=0
  tintcolor=#000000
  alpha=0
  autohide=0
  heightwhenhidden=1
  setdocktype=1
  setpartialstrut=1
  usefontcolor=0
  fontsize=12
  fontcolor=#ffffff
  usefontsize=0
  background=0
  backgroundfile=/usr/share/lxpanel/images/background.png
  iconsize=36
}
Plugin {
  type=space
  Config {
    Size=4
  }
}
Plugin {
  type=menu
  Config {
    image=start-here
    system {
    }
    separator {
    }
    item {
      name=Run...
      image=system-run
      command=run
    }
    separator {
    }
    item {
      name=Shutdown...
      image=system-shutdown
      command=logout
    }
  }
}
Plugin {
  type=space
  Config {
    Size=8
  }
}
Plugin {
  type=launchbar
  Config {
    Button {
      id=lxde-x-www-browser.desktop
    }
    Button {
      id=pcmanfm.desktop
    }
    Button {
      id=terminator.desktop
    }
  }
}
Plugin {
  type=space
  Config {
    Size=8
  }
}
Plugin {
  type=pager
  Config {
  }
}
Plugin {
  type=taskbar
  expand=1
  Config {
    tooltips=1
    IconsOnly=0
    ShowAllDesks=0
    UseMouseWheel=1
    UseUrgencyHint=1
    FlatButton=0
    MaxTaskWidth=200
    spacing=1
    GroupedTasks=0
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=cpu
  Config {
    ShowPercent=1
    Foreground=#a9a9a9a9a9a9
    Background=#d3d3d3d3d3d3
  }
}
Plugin {
  type=tray
  Config {
  }
}
Plugin {
  type=dclock
  Config {
    ClockFmt=%R
    TooltipFmt=%A %x
    BoldFont=0
    IconOnly=0
    CenterText=0
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=ejecter
  Config {
  }
}
' > $HOME/.config/lxpanel/LXDE/panels/panel
}

install_novnc() {
  $RUN apt-get install --no-install-recommends -y xauth x11-xkb-utils libxkbfile1 libxv1 libglu1-mesa libegl1-mesa python3-numpy

  TURBOVNC_VERSION=3.0.3
  VIRTUALGL_VERSION=3.1
  LIBJPEG_VERSION=2.1.5.1
  
  $RUN curl -O https://nchc.dl.sourceforge.net/project/turbovnc/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb
  $RUN curl -L -O https://nchc.dl.sourceforge.net/project/libjpeg-turbo/${LIBJPEG_VERSION}/libjpeg-turbo-official_${LIBJPEG_VERSION}_amd64.deb
  $RUN curl -O https://nchc.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb
 
  $RUN dpkg -i *.deb && $RUN rm -f *.deb
  #    rm -f /tmp/*.deb && \
  #    sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver
  
  # noVNC
  cd /opt/ && $RUN git clone https://github.com/novnc/noVNC.git 
  cd /opt/noVNC/utils && $RUN git clone https://github.com/novnc/websockify
}

install_ros() {
  ROS_DISTRO=$1
  sudo apt update && sudo apt install -y curl gnupg2 lsb-release
  sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
  sudo bash -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null'
  sudo apt update
  sudo apt install -y ros-${ROS_DISTRO}-desktop
  sudo apt install -y python3-pip
  pip3 install -U argcomplete
  
  # Install ROS 2 RQT
  sudo apt install -y ros-${ROS_DISTRO}-rqt
  
  # Install ROS 2 build tools
  sudo apt install -y python3-colcon-common-extensions python3-vcstool
}

main() {
  DEV=false; EDITOR=false; DECRYPT=false; FONTS=false; ZSH=false; PYTHON=false; ROS=false; NOVNC=false; NODE=false

  # Parse arguments
  while [ $# -gt 0 ]; do
    case $1 in
      --dev) DEV=true ;;
    esac
    case $1 in
      --editor) EDITOR=true ;;
    esac
    case $1 in
      --skip-decrypt) DECRYPT=false ;;
    esac
    case $1 in
      --dotfiles) ZSH=true ;;
    esac
    case $1 in
      --full) DEV=true; ZSH=true; ROS=true; NOVNC=true ;;
    esac
    case $1 in
      --fonts) FONTS=true ;;
    esac
    case $1 in
      --python) PYTHON=true
      PYTHON_VERSION="${2}"
      shift ;;
    esac
    case $1 in
      --ros) ROS=true
      ROS_DISTRO="${2}"
      shift ;;
    esac
    case $1 in
      --novnc) NOVNC=true ;;
    esac
    case $1 in
      --node) NODE=true
      NODE_VERSION="${2}"
      shift ;;
    esac
    shift
  done

  $RUN apt-get update

  install_tools
  install_xtools  

  if [ "$EDITOR" = true ]; then
    install_nvim
    #install_emacs
  fi

  if [ "$DEV" = true ]; then
    install_node "${NODE_VERSION:=20}"
    install_python "${PYTHON_VERSION:=3.11}"
    install_rust
    install_cpp
  fi

  if [ "$FONTS" = true ]; then
    install_fonts
  fi

  if [ "$PYTHON" = true ]; then
    install_python "${PYTHON_VERSION:=3.8.11}"
  fi

  if [ "$NODE" = true ]; then
    install_node "${NODE_VERSION:=20}"
  fi

  if [ "$ZSH" = true ]; then
    install_zsh
    install_yadm
    install_scripts
  fi

  if [ "$NOVNC" = true ]; then
    install_xtools
    install_fonts
    install_lxde
    install_novnc
  fi

  if [ "$ROS" = true ]; then
    install_ros "${ROS_DISTRO:=humble}"
  fi

  $RUN apt-get clean && \
    $RUN apt-get autoclean && \
    $RUN apt-get autoremove -y && \
    $RUN rm -rf /var/lib/apt/lists/* && \
    $RUN rm -rf /var/lib/cache/* && \
    $RUN rm -rf /var/lib/log/*
}

#main "$@"
main --editor --node 20 --python 3.11 --fonts 
