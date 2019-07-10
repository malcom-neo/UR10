# UR10

# To-do
1. add calibrate for zed camera

# aruco_pose_estimate
Dependant on [aruco_ros](https://github.com/pal-robotics/aruco_ros) package. Will be nice to have some filter

Markers pose and list of markers will be posted to /markers and /markerslist respectively

Changes: added broadcaster for tf and included in launch file.

Problems: unable to run rqt_tf_tree

# Moveit and moveit config
```
sudo apt-get install ros-kinetic-moveit
sudo apt-get install ros-kinetic-ur10-moveit-config
```

# Zed camera on cpu
[Github](https://github.com/willdzeng/zed_cpu_ros)

# fiducial
[Github](https://github.com/UbiquityRobotics/fiducials)



**Launch for gazebo**
```
roslaunch aruco_pose_estimation gazebo_recognition.launch
```

**Launch for hardware**

```
roslaunch aruco_pose_estimation multi_markers.launch
```

# ur10 gazebo simulation
**[Install gazebo_ros](http://gazebosim.org/tutorials?tut=ros_installing)**

**Getting markers model for gazebo**
1. Download [marker package](https://github.com/joselusl/aruco_gazebo)
2. Move markers file into ~/home/.gazebo/models

**Dependency**
1. [Universal robotics](https://github.com/ros-industrial/universal_robot). Build from scratch
2. Moveit!.
```
sudo apt-get install ros-melodic-moveit
```
3. joint-controller 
```

sudo apt-get install ros-melodic-joint-trajectory-controller
```
Unsure if that is the missing controller. If error appear while running, look for missing controller

**running UR10 gazebo**
Download ur10_simulation

```
roslaunch ur10_simulation gazebo.launch 
```

run your own movement script on another terminal to test on gazebo
