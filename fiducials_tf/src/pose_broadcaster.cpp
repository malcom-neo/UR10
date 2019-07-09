
#include <ros/ros.h>
#include <string>
#include <tf/transform_broadcaster.h>
#include <fiducial_msgs/FiducialTransformArray.h>
#include <geometry_msgs/Pose.h>

tf::Quaternion pitching_up(tf::Quaternion quat)
{
  quat = quat * tf::Quaternion(  0, 0.7071081, 0, -0.7071055 );
  quat = quat * tf::Quaternion(     0.7071081, 0, 0, -0.7071055 );
  return quat;
}


void poseCallback(const fiducial_msgs::FiducialTransformArrayConstPtr& msg){
  static tf::TransformBroadcaster br;
  tf::Transform transform;
  geometry_msgs::Transform pose;
  int size_of_array = (msg->transforms).size();
  for (int i=0 ;i<size_of_array;i++)
  {
    std::string markername = "marker:" + std::to_string(msg->transforms[i].fiducial_id);
    pose = msg->transforms[i].transform;

    tf::Transform transform;
    transform.setOrigin(tf::Vector3(pose.translation.x,pose.translation.y,pose.translation.z));

    tf::Quaternion quat;


    //aruco orientation require rotation as axis is in wrong direction
    tf::Quaternion before_rotation(pose.rotation.x,pose.rotation.y,pose.rotation.z,pose.rotation.w);
    tf::Quaternion after_rotation;
    after_rotation = pitching_up(before_rotation);
    transform.setRotation(after_rotation);

    br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "camera", markername));
    
  }
}


int main(int argc, char** argv){
  ros::init(argc, argv, "pose_broadcaster");

  ros::NodeHandle node;
  ros::Subscriber sub = node.subscribe("/fiducial_transforms", 10, &poseCallback);

  ros::spin();
  return 0;
};