import time
import os
import tkinter as tk
from tkinter import messagebox
from math import radians, degrees, pi
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

# Connect to real robot or simulate
def robot_online(online):
    print("Connecting to UR5e...")
    if online:
        robot.setConnectionParams('192.168.1.5', 30000, '/', 'anonymous', '')
        time.sleep(5)
        success = robot.ConnectSafe('192.168.1.5')
        time.sleep(5)
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY:
            raise Exception("Failed to connect: " + status_msg)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        print("Connection to UR5e Successful!")
    else:
        RDK.setRunMode(RUNMODE_SIMULATE)
        print("Simulation mode activated.")

# Move to initial position and show cube
def Init():
    print("Init")    
    robot.MoveL(init_t, True)
    print("Init_target REACHED")
    cube.setVisible(True)

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
    robot_online(False)  # True for real robot, False for simulation
    Init()
    Pick()
    Place()

# Run main and handle closing
if __name__ == "__main__":
    main()