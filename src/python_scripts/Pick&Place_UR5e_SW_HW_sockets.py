import os
import time
import socket
import tkinter as tk
from tkinter import messagebox
from math import radians, degrees, pi
import numpy as np
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to the .rdk file
relative_path = "src/roboDK/Pick&Place_UR5e.rdk"
SPEED = 20

# Start RoboDK with the project file
RDK = Robolink()
time.sleep(3)  # Wait for RoboDK to initialize

RDK.AddFile(os.path.abspath(relative_path))
time.sleep(2)  # Wait for the project to load

# Retrieve items from the RoboDK station
robot     = RDK.Item("UR5e")
tool      = RDK.Item("2FG7")
base      = RDK.Item("UR5e Base")
init_t    = RDK.Item("Init") #Traget del RoboDK
#app_pick  = RDK.Item("App_Pick")
pick_t    = RDK.Item("Pick") #Traget del RoboDK
#app_place = RDK.Item("App_Place")
place_t   = RDK.Item("Place") #Traget del RoboDK
table     = RDK.Item("Table")
cube      = RDK.Item("cube")

# Hide the cube initially
cube.setVisible(False)

# Set cube pose and parent
cube.setParent(table) #Do not maintain the actual absolute POSE
cube.setPose(pick_t.Pose())

# Set robot frame, tool and speed
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(SPEED)

# Robot Constants
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6
timel = 4

# URScript commands
set_tcp = "set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"
j1, j2, j3, j4, j5, j6 = np.radians(init_t.Joints()).tolist()[0]
movej_init = f"movej([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"
j1, j2, j3, j4, j5, j6 = np.radians(pick_t.Joints()).tolist()[0]
movej_pick = f"movej([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"
j1, j2, j3, j4, j5, j6 = np.radians(place_t.Joints()).tolist()[0]
movej_place = f"movej([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

# Check robot connection
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())

# Wait for robot response
def receive_response(t):
    try:
        print("Waiting time:", t)
        time.sleep(t)
    except socket.error as e:
        print(f"Error receiving data: {e}")
        exit(1)

# Move to initial position and show cube
def Init():
    print("Init")    
    robot.MoveL(init_t, True)
    print("Init_target REACHED")
    cube.setVisible(True)
    if robot_is_connected and UR5e_execution:
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_init)
        receive_response(timej)
    else:
        print("UR5e not connected. Simulation only.")

def Pick():
    print("Pick")
    robot.MoveL(pick_t)     # Mover robot al objeto
    cube.setParentStatic(tool)
    robot.MoveL(init_t)    # Mover robot a la posicion inicial
    print("Pick FINISHED")

def Place():     
    print("Place")
    robot.MoveL(place_t)
    cube.setParentStatic(table)
    robot.MoveL(init_t)    
    print("Place FINISHED")  

# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")                                                                           

def main():
    global robot_is_connected
    global UR5e_execution
    UR5e_execution = False  # Set to False to disenable UR5e execution
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)
    Init()
    Pick()
    Place()
    if robot_is_connected:
        robot_socket.close()

# Run main and handle closing
if __name__ == "__main__":
    main()