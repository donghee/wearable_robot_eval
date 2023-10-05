#! /usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time

class EffortTestNode(Node):

    def __init__(self):
        super().__init__('effort_test_node')
        self.publisher_ = self.create_publisher(Float64MultiArray, '/effort_controller/commands', 10)
        self.get_logger().info('node created')
        
        commands = Float64MultiArray()
        commands.data.append(0.0)
        self.publisher_.publish(commands)
        time.sleep(1)

        commands.data[0] = 100.0
        self.publisher_.publish(commands)
        time.sleep(1)

        #  commands.data[0] = -100.0
        #  self.publisher_.publish(commands)
        #  time.sleep(1)
        #
        #  commands.data[0] = 0.0
        #  self.publisher_.publish(commands)
        #  time.sleep(1)
        
def main(args=None):
    rclpy.init(args=args)

    effort_test_node = EffortTestNode()

    rclpy.spin(effort_test_node)
    effort_test_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

