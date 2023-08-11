import os
import signal
import subprocess
import time
from wearable_robot_evaluation.wearability.simulation_modify_2 import test_safety
from wearable_robot_evaluation.interactivity.interaction_score import test_interactivity

def stop_process(proc, timeout=10):
    pgid = os.getpgid(proc.pid)
    time.sleep(timeout)
    os.killpg(pgid, signal.SIGINT)
    time.sleep(1)
    os.killpg(pgid, signal.SIGINT)
    os.system('pkill gzclient')
    proc.wait()

# Run simulation
evaluation_proc = subprocess.Popen(['ros2', 'launch', 'wearable_robot_gazebo', 'evaluation.launch.py'], start_new_session=True)
stop_process(evaluation_proc, 10)

# Wearability
os.system('clear')
print("Start Wearability")
test_safety(0.0, 150.0)
print("Finish Wearability")
time.sleep(2)

# Interactivity
os.system('clear')
print("Start Interactivity")
test_interactivity()
print("Finish Interactivity")
time.sleep(5)

# Usability
#pushd ./wearable_robot_evaluation/usability
#./act-r.sh 10

#print("Finish Evaluation")
