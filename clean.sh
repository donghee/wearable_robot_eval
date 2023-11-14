fastdds shm clean
ps aux | grep ros2 | awk '{ print $2 }' | xargs -n 1 kill -9 
