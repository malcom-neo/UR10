#include <ros/ros.h>
#include "std_msgs/String.h"
#include <geometry_msgs/Pose.h>

class BaseToCam
{
private:
  ros::Publisher BaseToMarker;
  ros::Subscriber eefPose;
  ros::Subscriber MarkerPose;
  float pub_rate_Hz = 0.66;
  ros::NodeHandle n;

  void initializeBaseToMarker();

public:
 BaseToCam(){
   initializeBaseToMarker();

 }
};

void BaseToCam::initializeBaseToMarker()
{
  BaseToMarker = n.advertise<geometry_msgs::Pose>("/base_to_object",10);
  ros::Rate pub_rate(pub_rate_Hz);
  geometry_msgs::Pose msg;
  msg.position.x = 1;
  BaseToMarker.publish(msg);

}




int main(int argc, char** argv)
{
  ros::init(argc, argv, "robot_base_to_cam_tf");
  BaseToCam node;
  ros::spin();
}
