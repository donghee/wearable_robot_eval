#!/usr/bin/python
import pyfirmata
import time
 
board = pyfirmata.Arduino('/dev/ttyACM0')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
pin9 = board.get_pin('d:9:s')
 
def move_servo(a):
    pin9.write(a)
 
move_servo(0);
time.sleep(2)
move_servo(90);
time.sleep(2)
move_servo(180);
time.sleep(2)
move_servo(90);
time.sleep(2)
move_servo(0);
time.sleep(2)
