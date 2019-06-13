# UR10

# To-do
1. add flags to stop movement in eef_tracking when movement fail 
2. eef code to follow camera pose message
3. merge launch file, currently linking here and there for no reason
4. failsafe for collision with box
5. Rotate of orientation from marker to eef




# aruco_pose_estimate
Dependant on aruco_ros package.

Markers pose and list of markers will be posted to /markers and /markerslist respectively

Changes: added broadcaster for tf and included in launch file.

Problems: unable to run rqt_tf_tree

** Launch for gazebo **
```
roslaunch aruco_pose_estimation gazebo_recognition.launch
```

** Launch for hardware **

```
roslaunch aruco_pose_estimation multi_markers.launch
```

# ur_simulation

** Getting markers model for gazebo **
1. Download [marker package](https://github.com/joselusl/aruco_gazebo)
2. Move markers file into ~/home/.gazebo/models


** Launch gazebo, ur10 and controller **
```
roslaunch ur_gazebo gazebo.launch 
```

run movement script to test on gazebo
