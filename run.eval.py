import os
import signal
import subprocess
import time
from time import sleep
from wearable_robot_evaluation.wearability.simulation_modify_2 import test_safety
from wearable_robot_evaluation.interactivity.interaction_score import test_interactivity

def kill_process(proc, timeout=10):
    pgid = os.getpgid(proc.pid)
    time.sleep(timeout)
    os.killpg(pgid, signal.SIGINT)
    time.sleep(2)
    os.killpg(pgid, signal.SIGINT)
    os.system('pkill gzclient')
    proc.wait()

# Run simulation
evaluation_proc = subprocess.Popen(['ros2', 'launch', 'wearable_robot_gazebo', 'evaluation.launch.py'], start_new_session=True)
kill_process(evaluation_proc, 80)
