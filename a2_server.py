from bluetooth import *
import sys
import logging
from time import sleep
from pprint import pprint

import bluepy
import ezst

# Handle the socket connection
# Send light sensor when a message is received
def handle_connection(socket):
    while True:
        try:
            d= socket.recv(1024)
            if d:
                STATE = "run" if tag.read_light() > 0 else "stop"
                socket.send(STATE)
        except Exception as e:
            print("Error: " + str(e))
            break


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Mac address of the sensor tag
    # Initialize and connect to sensor tag
    MAC = "F0:F8:F2:86:39:87"
    tag = ezst.EasySensorTag(MAC, debug=logging.DEBUG)
    tag.init_sensors()
    print("FW version: ", tag.firmware)
    print("Tag Connected")


    # Initialize and run bluetooth socket server
    port =2
    backlog=1
    serverSocket=BluetoothSocket(RFCOMM)
    serverSocket.bind(("",port))
    serverSocket.listen(backlog)
    print("Server Starting")
    # Accept incoming connections and handle them
    while tag.is_alive:
        socket, client_info = serverSocket.accept()
        print("Accepted connection from ", client_info)
        handle_connection(socket)
        socket.close()



    serverSocket.close()
