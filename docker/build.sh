# root
#docker build -t ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc . -f Dockerfile

# user
docker build -t ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc_user_$USER --build-arg="UID=$(id -u)" --build-arg="GID=$(id -g)" --build-arg="USER=$USER" --build-arg="HOME=$HOME" . -f Dockerfile
