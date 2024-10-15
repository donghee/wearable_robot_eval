# root
#docker build -t ghcr.io/donghee/wearable_robot_eval:foxy . -f Dockerfile

# user
docker build -t ghcr.io/donghee/wearable_robot_eval:foxy --build-arg="UID=$(id -u)" --build-arg="GID=$(id -g)" --build-arg="USER=$USER" --build-arg="HOME=$HOME" . -f Dockerfile
