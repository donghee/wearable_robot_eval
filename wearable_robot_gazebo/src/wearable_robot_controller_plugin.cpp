#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

namespace gazebo
{
  class WearableRobot : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      this->model = _parent;

      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&WearableRobot::OnUpdate, this));
    }

    public: void OnUpdate()
    {
      this->model->GetLink("link")->SetForce(ignition::math::Vector3d(1.0, 0.0, 0.0));
    }

    private: physics::ModelPtr model;

    private: event::ConnectionPtr updateConnection;
  };

  GZ_REGISTER_MODEL_PLUGIN(WearableRobot)
}
