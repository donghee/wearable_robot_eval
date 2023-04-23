#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

#include <gazebo_ros/node.hpp>


namespace gazebo
{
  class WearableRobot : public ModelPlugin
  {

    gazebo_ros::Node::SharedPtr ros_node_;
    ignition::math::Vector3d force_;

    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
    {
      this->ros_node_ = gazebo_ros::Node::Get(_sdf);
      this->force_ = ignition::math::Vector3d(0, 0, 0);

      if (_sdf->HasElement("force")) {
        this->force_ = _sdf->Get<ignition::math::Vector3d>("force");
        RCLCPP_INFO(
            this->ros_node_->get_logger(),
            "Set Force: %f %f %f", this->force_.X(), this->force_.Y(), this->force_.Z());
      }

      this->model = _parent;

      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&WearableRobot::OnUpdate, this));
    }

    public: void OnUpdate()
    {
      this->model->GetLink("link")->SetForce(this->force_);

      ignition::math::Vector3d relative_force = this->model->GetLink("link")->RelativeForce();

      RCLCPP_INFO(
          this->ros_node_->get_logger(),
          "Read Force: %f %f %f", relative_force.X(), relative_force.Y(), relative_force.Z());
    }

    private: physics::ModelPtr model;

    private: event::ConnectionPtr updateConnection;
  };

  GZ_REGISTER_MODEL_PLUGIN(WearableRobot)
}
