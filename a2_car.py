#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from bluetooth import *
import threading

# state constants
ON = True
OFF = False

'''
Functions for displaying messages on the brick provided within ev3 docs and hello world example
'''

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


# Print a message to the screen of the brick
def printMsg(msg):
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')
    print(msg)

# Move the motor for a specified number of rotations
def move(motor):
    motor.on_for_rotations(SpeedPercent(10), 1)

def main():
    # MAC Address of the Pi and port bluetooth socket server is running on
    server_address = "B8:27:EB:E8:5B:F8"
    port=2

    # Create the bluetooth socket and connect to the server running on the pi
    sock = BluetoothSocket(RFCOMM)

    sock.connect((server_address, port))

    # Initialize motors on the ev3
    m1 = LargeMotor(OUTPUT_B)
    m2 = LargeMotor(OUTPUT_A)


    # Exectuion loop
    while True:
        try:
            # Send a messgae to receive the state of the sensor
            sock.send("get")
            data = sock.recv(1024).decode("utf-8")
            # Print state on the ev3
            printMsg(data)
            # If the data is run spin the motors in seperate threads to allow both motors
            # to run concurrently, the join threads to wait for execution to be concluded before moving on
            if data == "run":
                left = threading.Thread(target=move, args=(m1,))
                right = threading.Thread(target=move, args=(m2,))
                left.start()
                right.start()
                left.join()
                right.join()
        except Exception as e:
            printMsg(e)
            time.sleep(5)
            break

    sock.close()

if __name__ == '__main__':
    main()
