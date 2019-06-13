#!/usr/bin/env python



import sys
import os 
import copy
import rospy
import yaml
import signal
import datetime
from time import sleep
from termcolor import colored

import moveit_commander
import moveit_msgs.msg
from moveit_commander.conversions import pose_to_list
import geometry_msgs.msg
import tf
from  ur10_rmf.arm_manipulation import ArmManipulation
from  ur10_rmf.arm_manipulation import changeInOrientation

import numpy as np
from math import pi

from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import Float32MultiArray # temp solution
from geometry_msgs.msg import Pose2D
# from dynamixel_gripper.msg  import grip_state
from rm_msgs.msg import grip_state
from rm_msgs.msg import ManipulatorState

#----------------------------------------------------------
""" To Do:

1. make sure that during loading and unloading, when 1 movement fails, there is a feedback so that it wont skip that movement and fuck things up

2. add lifting height to yaml file to make it robust

3.gazebo simulate
  


"""



# ***************************************************************************************************************

class RobotManipulatorControl():
  def __init__(self):

    rospy.init_node('robot_manipulator_control_node', anonymous=True)
    self.ur10 = ArmManipulation()   
    self.scene = moveit_commander.PlanningSceneInterface()
    self.br = tf.TransformBroadcaster()
    self.listener = tf.TransformListener()
    
    #default starting location to prevent colision and look nice
    self.default_joint = [-0.10146845329546418, -1.7705691186441455, 2.1581055010616392, -0.3874414905316692, 1.4692307403748652, -3.1408828576165577]
    #default starting location for the unloading part
    self.unloading_joint = [3, -1.7705691186441455, 2.1581055010616392, -0.3874414905316692, 1.4692307403748652, -3.1408828576165577]
    self.ur10.go_to_joint_state(self.default_joint,2)
    
    #load yaml marker config file
    self.loadconfig()
    #self.set_constrains()

    #default param
    self.timeout = 5
        

  def set_constrains(self):
    #set contrains to make sure that the eef is always level
    #https://answers.ros.org/question/174095/end-effector-pose-constrained-planning/
    self.constraints = moveit_msgs.msg.Constraints()
    self.eef_constraint = moveit_msgs.msg.OrientationConstraint()
    self.eef_constraint.header.frame_id = "base_link"
    self.eef_constraint.link_name = "ee_link"
    self.eef_constraint.orientation = changeInOrientation(0,0,0,0)
    self.eef_constraint.absolute_x_axis_tolerance = 6.28
    self.eef_constraint.absolute_y_axis_tolerance = 6.28
    self.eef_constraint.absolute_z_axis_tolerance =  6.28
    self.eef_constraint.weight = 1
    self.constraints.orientation_constraints.append(self.eef_constraint)
    self.ur10.group.set_path_constraints(self.constraints)



  def addmarker(self,position_list,count):
    rospy.sleep(1.5)
    marker_name = "marker"+str(count) 
    print("adding marker" + str(count))
    box = geometry_msgs.msg.PoseStamped()
    box.header.frame_id = "base_link"
    box.pose.orientation =changeInOrientation(0,position_list[3],
                                                position_list[4],
                                                position_list[5])
    box.pose.position.x = position_list[0]
    box.pose.position.y = position_list[1]
    box.pose.position.z = position_list[2]
    self.scene.add_box(marker_name, box, size=(0.01, 0.32, 0.32))
    return self.check_marker(marker_name)


  def check_marker(self,marker_name):
    if (len(self.scene.get_attached_objects([marker_name]))>0):
      return True
    else:
      return False
    

  def removemarker(self, count):
    marker_name = "marker"+str(count)
    self.scene.remove_world_object(marker_name)
    return not(self.check_marker(marker_name))


  def loadconfig(self):
    directory =  "/"+	str(os.path.dirname(os.path.abspath(__file__)).strip("src/ObjTrack")) + "s/src/ObjTrack/config/markerposition.yaml" #disgusting
    with open(directory, 'r') as directory:
      data = yaml.load(directory)
      self.markerconfig = data["marker_position"]
      self.loading_position = data["loading_position"]
      self.fork_length = data["fork_length"]


      
  def pick_up(self,marker_position):
    #for all movement pick_up and unload, at the end of function, it will return to face the shelf
	#lining up the fork. hardcoded position, fine tune with vision
    marker_position[0] -= (self.fork_length+0.05)
    marker_position[2] += 0.05
    self.ur10.go_to_pose_goal(marker_position,2)

    #hardcoded to slide in the fork
    marker_position[0] += (self.fork_length+0.05)
    self.ur10.go_to_pose_goal(marker_position,2)

    #hardcoded to lift up the fork
    marker_position[2] += 0.05
    self.ur10.go_to_pose_goal(marker_position,2)

    #pull out from shelf
    marker_position[0] -= (self.fork_length+0.05)
    self.ur10.go_to_pose_goal(marker_position,2)

    #go back to default position
    self.ur10.go_to_joint_state(self.default_joint,2)


  def unloading_item(self,marker_position):
    self.ur10.go_to_joint_state(self.unloading_joint,2)

    #lining up
    marker_position[0] += (self.fork_length+0.05)
    marker_position[2] += 0.05
    self.ur10.go_to_pose_goal(marker_position,2)

    #hardcoded to slide in the fork
    marker_position[0] -= (self.fork_length+0.05)
    self.ur10.go_to_pose_goal(marker_position,2)

    #hardcoded to lift up the fork
    marker_position[2] += 0.05
    self.ur10.go_to_pose_goal(marker_position,2)

    #pull out from shelf
    marker_position[0] -= (self.fork_length+0.05)
    self.ur10.go_to_pose_goal(marker_position,2)

    #go back to default position
    self.ur10.go_to_joint_state(self.unloading_joint,2)
    self.ur10.go_to_joint_state(self.default_joint,2)


  def start_visualisation(self):
    while True:
      user_input = int(raw_input(colored("enter marker number, 0 to unload","red","on_green")))
      print(colored("moving to marker:"+str(user_input),"white","on_green"))
      if (user_input in self.markerconfig.keys()) or (user_input == 0) :
        try:
          marker_position =  self.markerconfig[user_input]
        except:
          marker_position = self.loading_position

        #if the goal is to turn around, the starting point will be 180 degree
        if user_input == 0 :
          print(colored("unloading","white","on_green"))
          self.unloading_item(marker_position)

        else:
          print(colored("loading", "white", "on_green"))
          self.pick_up(marker_position)
      else:
        print(colored("marker not defined","white","on_green"))
		




#################################################################################################################
##################################################################################################################



def signal_handler(sig, frame):
  print('You pressed Ctrl+C!, end program...')
  sys.exit(0)


if __name__ == '__main__':
  print(colored("  -------- Begin Python Moveit Script --------  " , 'white', 'on_green'))
  signal.signal(signal.SIGINT, signal_handler)
  robot_manipulator_control = RobotManipulatorControl()
  
  robot_manipulator_control.start_visualisation()
  #robot_manipulator_control.ur10.go_to_joint_state(robot_manipulator_control.unloading_joint,2)