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

print("동작 수행에 따른 데이터 저장 완료")
print("-----------------------------")
input("\nPress enter to continue...\n")

# Wearability
os.system('clear')
print("Start Wearability")
test_safety(0.0, 150.0)
print("Finish Wearability")

print("-----------------------------")
input("\nPress enter to continue...\n")

# Interactivity
os.system('clear')
print("Start Interactivity")
test_interactivity()
print("Finish Interactivity")

print("-----------------------------")
input("\nPress enter to continue...\n")

# Usability
os.system('clear')
print("Start Usability")
usability_proc = subprocess.Popen(['./act-r.sh', '10'], cwd='./wearable_robot_evaluation/usability', stdin=subprocess.PIPE)
time.sleep(2)
usability_proc.stdin.write(b'(load "/home/donghee/src/wearable_robot_act-r/tmp/actr7.x/usability/system_interface.lisp")\n')
time.sleep(1)
#usability_proc.stdin.write(b'(run-the-model-until-time 10 (list \"arm\" \"adaptive\") 39 \"high\" nil 20 5)\n')
usability_proc.stdin.write(b'(run-the-model-until-time 10 (list "arm" "adaptive") 39 "high" nil 20 5)\n')
usability_proc.stdin.close() # Send EOF to stop ACT-R
time.sleep(2)
print("Finish Usability")

print("-----------------------------")
input("\nPress enter to continue...\n")

print("Finish Evaluation")
