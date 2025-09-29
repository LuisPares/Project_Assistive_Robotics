from robodk import robolink, robomath
from robodk.robomath import radians, degrees
import time

# Robot setup
RDK = robolink.Robolink()
robot = RDK.Item('UR5e')
base = RDK.Item('UR5e Base')
tool = RDK.Item('2FG7')
Init_target = RDK.Item('Init')
pick_target = RDK.Item('Pick')
App_target = RDK.Item('App')
Place_target = RDK.Item('Place')
App_place_target = RDK.Item('App Place')
cube = RDK.Item('Cube')
table = RDK.Item('Table')
cube.setVisible(False)
cube_pose = RDK.Item('Pose')
cube_pose.setParent(table)
cube_pose.setPose(cube_pose.Pose())
cube.setPose(cube_pose.Pose())
cube.setVisible(True)

robot.setPoseFrame(base)
robot.setPoseTool(tool)

def Init():
    robot.MoveJ(Init_target, True)
    print("Init")

def Pick():
    robot.MoveJ(pick_target, True)
    print("Pick")

    ...
    cube.setParentStatic(tool#Maintain the relative
    robot.MoveL(App_static_tool_target, True)
    print("Pick FINISHED")

def Place():                                                                                                                                                                                                                                                                                def main():                                                                Init()                                                                 Pick()                                                                 Place()                                                                                                                                   if __main__=="__main__":                                                   main()                                                                               
