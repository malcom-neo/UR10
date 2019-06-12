#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <aruco_msgs/MarkerArray.h>
#include <geometry_msgs/Pose.h>


void poseCallback(const aruco_msgs::MarkerArrayConstPtr& msg){
  static tf::TransformBroadcaster br;
  tf::Transform transform;
  geometry_msgs::Pose pose;
  //std::cout<< msg->markers[0] << std::endl;
  int size_of_array = (msg->markers).size();
  //std::cout<< size_of_array <<std::endl;
  for (int i=0 ;i<size_of_array;i++)
  {
    std::string markername = "marker:" + std::to_string(msg->markers[i].id);
    pose = msg->markers[i].pose.pose;

    tf::Transform transform;
    transform.setOrigin(tf::Vector3(pose.position.x,pose.position.y,pose.position.z));


    transform.setRotation(tf::Quaternion(pose.orientation.x,pose.orientation.y,pose.orientation.z,pose.orientation.w));

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
