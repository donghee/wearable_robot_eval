#!/usr/bin/python3.8

import logging
import os
import signal
import subprocess
import sys
import psutil
import time

FIFO_RX_FILE = '/tmp/wde_ros_tx'
FIFO_TX_FILE = '/tmp/wde_ros_rx'

manager_logger = logging.getLogger('ros_manager')

def init_fifo():
    if not os.path.exists(FIFO_TX_FILE):
        os.mkfifo(FIFO_TX_FILE)
    if not os.path.exists(FIFO_RX_FILE):
        os.mkfifo(FIFO_RX_FILE)

def kill_processes(pid):
    def on_terminate(proc):
        print("process {} terminated with exit code {}".format(proc, proc.returncode))
    '''Kills parent and children processess'''

    os.system('pkill -SIGTERM gzclient')
    #os.system('pkill -SIGKILL gzclient')
    os.system('pkill -SIGTERM gzserver')
    #os.system('pkill -SIGKILL gzserver')
    time.sleep(2)

    parent = psutil.Process(pid)
    children = parent.children(recursive=True)

    # kill all the child processes
    for child in children:
        print(child)
        child.terminate()
    _, still_alive = psutil.wait_procs(children, timeout=3, callback=on_terminate )
    for child in still_alive:
        child.kill()

    # kill the parent process
    print(parent)
    parent.kill()

def start_wearable_evaluation(device="upper", code="1"):
    manager_logger.info('start wearable evaluation')
    #subprocess.call(['gnome-terminal', '--', 'bash', '-c', 'cd ~/ros2_ws/src/wearabie_robot_eval && ./run_eval_human_66dof.sh'])
#    wearable_eval_proc = subprocess.call(['terminator', '-x', 'bash', '-c', '~/ros2_ws/src/wearable_robot_eval/run_eval_human_66dof.sh; read -p \"Press any key... \" -n1'])
    if device == "upper":
        control_type = "square_wave"
        if code == "1":
            control_type = "square_wave"
        else: # TODO
            control_type = "square_wave_failed"

        cmd = ['bash', '-c', f'cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo human_45dof_wearing_upper_limb_effort_control.launch.py control_type:={control_type}']
    else:
        control_type = "normal"
        if code == "1":
            control_type = "normal"
        elif code =="2":
            control_type = "torque_limit"
        elif code =="3":
            control_type = "rom_limit"

        cmd = ['bash', '-c', f'cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo human_45dof_wearing_lower_limb_position_control.launch.py control_type:={control_type}']
    try:
        wearable_eval_proc = subprocess.Popen(cmd, start_new_session=True)
        wearable_eval_proc.wait(timeout=25)
    except subprocess.TimeoutExpired:
        print('Evaluation Timeout', file=sys.stderr)
        kill_processes(wearable_eval_proc.pid)
        with open(FIFO_TX_FILE, 'w') as fifo:
            fifo.write('finish')
            return

    with open(FIFO_TX_FILE, 'w') as fifo:
        fifo.write('error')

def listen_ros_command():
    if not os.path.exists(FIFO_RX_FILE):
        return

    while True:
        with open(FIFO_RX_FILE, 'r') as fifo:
            line = fifo.readline()
            print(line)
            if line.startswith('start'):
                code = line.split()[-1]
                if 'upper' in line:
                    start_wearable_evaluation('upper', code)
                if 'lower' in line:
                    start_wearable_evaluation('lower', code)



if __name__ == '__main__':
    init_fifo()
    listen_ros_command()
