#!/usr/bin/python3.8


import logging
import os
import signal
import subprocess
import sys

FIFO_RX_FILE = '/tmp/wde_ros_tx'
FIFO_TX_FILE = '/tmp/wde_ros_rx'

manager_logger = logging.getLogger('ros_manager')

def init_fifo():
    if not os.path.exists(FIFO_TX_FILE):
        os.mkfifo(FIFO_TX_FILE)
    if not os.path.exists(FIFO_RX_FILE):
        os.mkfifo(FIFO_RX_FILE)

def start_wearable_evaluation(device="upper"):
    manager_logger.info('start wearable evaluation')
    #subprocess.call(['gnome-terminal', '--', 'bash', '-c', 'cd ~/ros2_ws/src/wearabie_robot_eval && ./run_eval_human_66dof.sh'])
#    wearable_eval_proc = subprocess.call(['terminator', '-x', 'bash', '-c', '~/ros2_ws/src/wearable_robot_eval/run_eval_human_66dof.sh; read -p \"Press any key... \" -n1'])
    if device == "upper":
        cmd = ['bash', '-c', 'cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo human_45dof_wearing_upper_limb_effort_control.launch.py']
    else:
        cmd = ['bash', '-c', 'cd ~/ros2_ws && colcon build && source ./install/setup.bash && ros2 launch wearable_robot_gazebo human_45dof_wearing_lower_limb_position_control.launch.py']
    try:
        wearable_eval_proc = subprocess.Popen(cmd, start_new_session=True)
        wearable_eval_proc.wait(timeout=25)
    except subprocess.TimeoutExpired:
        print('Evaluation Timeout', file=sys.stderr)
        os.killpg(os.getpgid(wearable_eval_proc.pid), signal.SIGTERM)
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
                if 'upper' in line:
                    start_wearable_evaluation('upper')
                if 'lower' in line:
                    start_wearable_evaluation('lower')



if __name__ == '__main__':
    init_fifo()
    listen_ros_command()