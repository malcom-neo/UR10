#include <ros/ros.h>
#include <string>
#include <tf/transform_broadcaster.h>
#include <aruco_msgs/MarkerArray.h>
#include <geometry_msgs/Pose.h>

tf::Quaternion pitching_up(tf::Quaternion quat)
{
  quat = quat * tf::Quaternion(  0.7071068, 0, 0, 0.7071068);
  quat = quat * tf::Quaternion(   0, 0.7071068, 0, 0.7071068);
  return quat;
}


void poseCallback(const aruco_msgs::MarkerArrayConstPtr& msg){
  static tf::TransformBroadcaster br;
  tf::Transform transform;
  geometry_msgs::Pose pose;
  int size_of_array = (msg->markers).size();
  for (int i=0 ;i<size_of_array;i++)
  {
    std::string markername = "marker:" + std::to_string(msg->markers[i].id);
    pose = msg->markers[i].pose.pose;

    tf::Transform transform;
    transform.setOrigin(tf::Vector3(pose.position.x,pose.position.y,pose.position.z));

    tf::Quaternion quat;


    //aruco orientation require rotation as axis is in wrong direction
    tf::Quaternion before_rotation(pose.orientation.x,pose.orientation.y,pose.orientation.z,pose.orientation.w);
    tf::Quaternion after_rotation;
    after_rotation = pitching_up(before_rotation);
    transform.setRotation(after_rotation);

    br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "camera", markername));
    
  }
}


int main(int argc, char** argv){
  ros::init(argc, argv, "pose_broadcaster");

  ros::NodeHandle node;
  ros::Subscriber sub = node.subscribe("/aruco_marker_publisher/markers", 10, &poseCallback);

  ros::spin();
  return 0;
};
