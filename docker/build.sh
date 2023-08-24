# root
docker build -t ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc . -f Dockerfile

# user
docker build -t ghcr.io/donghee/wearable_robot_eval:foxy_nvidia_novnc_user --build-arg="USER=donghee" --build-arg="HOME=/home/donghee" . -f Dockerfile
