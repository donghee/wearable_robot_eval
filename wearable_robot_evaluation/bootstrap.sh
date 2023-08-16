#!/bin/sh

# Requirements for Evaluation Tools
# Deepmimic: Python 3.7

curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

. ~/.bashrc

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

pyenv init -
pyenv virtualenv-init -

pyenv install 3.7.17
pyenv global 3.7.17

# Wearability, Interactivity: python-tkinter, pandas, scipy, numpy matplotlib
sudo apt-get update; sudo apt-get install python3-tk libbz2-dev -y
bash -c "pip3 install pandas scipy numpy matplotlib"

# Usability: sbcl, quicklisp
cd /tmp
wget http://prdownloads.sourceforge.net/sbcl/sbcl-2.0.9-x86-64-linux-binary.tar.bz2
tar -xf sbcl-2.0.9-x86-64-linux-binary.tar.bz2 && rm sbcl-2.0.9-x86-64-linux-binary.tar.bz2
cd sbcl-2.0.9-x86-64-linux && sudo sh install.sh && cd .. && rm -r sbcl-2.0.9-x86-64-linux
wget https://beta.quicklisp.org/quicklisp.lisp && sbcl --quit --load quicklisp.lisp --eval '(quicklisp-quickstart:install :path "quicklisp")' && rm quicklisp.lisp
