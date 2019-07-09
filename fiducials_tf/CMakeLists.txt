cmake_minimum_required(VERSION 2.8.3)
project(fiducials_tf)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${DEPRECATION_FLAG} -std=c++14 -w")
set(CMAKE_VERBOSE_MAKEFILE OFF)
set(CMAKE_RULE_MESSAGES OFF)

add_definitions(-std=c++14 -Wall -Werror)

find_package(OpenCV REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  dynamic_reconfigure
  geometry_msgs
  image_transport
  roscpp
  rospy
  tf
  fiducial_msgs
  sensor_msgs
  visualization_msgs
)

catkin_package(
  #INCLUDE_DIRS include
  #LIBRARIES aruco_ros_utils
  CATKIN_DEPENDS sensor_msgs tf 
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(fiducials_tf src/pose_broadcaster.cpp)
target_link_libraries(fiducials_tf ${catkin_LIBRARIES})
#add_dependencies(sub beginner_tutorials_generate_messages_cpp)
