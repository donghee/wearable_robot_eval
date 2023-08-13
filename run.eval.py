import os
import signal
import subprocess
import time
from time import sleep
from tqdm import tqdm
from wearable_robot_evaluation.wearability.simulation_modify_2 import test_safety
from wearable_robot_evaluation.interactivity.interaction_score import test_interactivity

def stop_process(proc, timeout=10):
    pgid = os.getpgid(proc.pid)
    time.sleep(timeout)
    os.killpg(pgid, signal.SIGINT)
    time.sleep(2)
    os.killpg(pgid, signal.SIGINT)
    os.system('pkill gzclient')
    proc.wait()


# Run simulation
evaluation_proc = subprocess.Popen(['ros2', 'launch', 'wearable_robot_gazebo', 'evaluation.launch.py'], start_new_session=True)
stop_process(evaluation_proc, 80)

# Wearability
os.system('clear')
print("Start Wearability")
test_safety(0.0, 150.0)
print("Finish Wearability")
#time.sleep(2)
for i in tqdm(range(5)):
    sleep(1)

# Interactivity
os.system('clear')
print("Start Interactivity")
test_interactivity()
print("Finish Interactivity")
#time.sleep(5)
for i in tqdm(range(5)):
    sleep(1)

# Usability
os.system('clear')
print("Start Usability")
usability_proc = subprocess.Popen(['./act-r.sh', '10'], cwd='./wearable_robot_evaluation/usability', stdin=subprocess.PIPE)
usability_proc.stdin.write(b'\x04') # Send ctrl+d to stop ACT-R
time.sleep(2)
print("Finish Usability")
for i in tqdm(range(5)):
    sleep(1)

print("Finish Evaluation")