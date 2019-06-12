# UR10

# To-do
1. add flags to stop movement in eef_tracking when movement fail 
2. eef code to follow camera pose message
3. merge launch file, currently linking here and there for no reason
4. failsafe for collision with box




# aruco_pose_estimate
Dependant on aruco_ros package

Changes: added broadcaster for tf and included in launch file.

Problems: unable to run rqt_tf_tree

# ur_simulation
launch gazebo, ur10 and controller using 
```
roslaunch ur_gazebo gazebo.launch 
```
run script then to test on gazebo
