#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

#include <gazebo_ros/node.hpp>
#include <string>

namespace gazebo
{
  class WearableRobot : public ModelPlugin
  {

    gazebo_ros::Node::SharedPtr ros_node_;
    ignition::math::Vector3d force_;
    std::string link_;
    std::ofstream csv_file_;

    public: WearableRobot() {
      csv_file_.open("/tmp/human.csv");
      csv_file_ << "t, x, y, z\n";
    }

    public: ~WearableRobot() {
      csv_file_.close();
    }

    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
    {
      this->ros_node_ = gazebo_ros::Node::Get(_sdf);
      this->force_ = ignition::math::Vector3d(0, 0, 0);
      this->link_ = "";

      if (_sdf->HasElement("force")) {
        this->force_ = _sdf->Get<ignition::math::Vector3d>("force");
        RCLCPP_INFO(
            this->ros_node_->get_logger(),
            "Set Force: %f %f %f", this->force_.X(), this->force_.Y(), this->force_.Z());
      }

      if (_sdf->HasElement("link")) {
        this->link_ = _sdf->Get<std::string>("link");
        RCLCPP_INFO(
            this->ros_node_->get_logger(),
            "Get Link Name: %s", this->link_.c_str());
      }

      this->model = _parent;

      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&WearableRobot::OnUpdate, this));
    }

    public: void OnUpdate()
    { 
      physics::WorldPtr world = this->model->GetWorld();
      common::Time current_time = world->SimTime(); 

      this->model->GetLink(this->link_)->SetForce(this->force_);

      ignition::math::Vector3d relative_force = this->model->GetLink(this->link_)->RelativeForce();

      RCLCPP_INFO(
          this->ros_node_->get_logger(),
          "Read Force: %f %f %f", relative_force.X(), relative_force.Y(), relative_force.Z());

      csv_file_ << current_time.Double() << "," << relative_force.X() << "," <<  relative_force.Y() << "," << relative_force.Z() << "\n";
    }

    private: physics::ModelPtr model;

    private: event::ConnectionPtr updateConnection;
  };

  GZ_REGISTER_MODEL_PLUGIN(WearableRobot)
}
