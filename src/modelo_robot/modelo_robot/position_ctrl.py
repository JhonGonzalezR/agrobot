#!/usr/bin/env python3
#Librerias de ROS2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
#Librerias de Python
import math

class JointAnglePositionPublisher(Node):
    def __init__(self):
        super().__init__('joint_angle_publisher')

        self.rueda_izq_delantera_joint_current_angle = math.radians(0)
        self.rueda_der_delantera_joint_current_angle = math.radians(0)
        self.rueda_izq_trasera_joint_current_angle = math.radians(0)
        self.rueda_der_trasera_joint_current_angle = math.radians(0)
        self.aspersor_joint_current_angle = math.radians(0)

        self.rueda_izq_delantera_joint_final_angle = math.radians(15)
        self.rueda_der_delantera_joint_final_angle = math.radians(15)
        self.rueda_izq_trasera_joint_final_angle = math.radians(15)
        self.rueda_der_trasera_joint_final_angle = math.radians(15)
        self.aspersor_joint_final_angle = math.radians(15)

        self.angle_publisher = self.create_publisher(Float64MultiArray, "/joint_position_controller/commands", 10)
        self.angle_msg = Float64MultiArray()
        self.interpolation_timer = self.create_timer(0.1, self.publish_angle_position_in_joints)
    
    def publish_angle_position_in_joints(self):
        self.rueda_izq_delantera_joint_current_angle += 0.01
        self.rueda_der_delantera_joint_current_angle += 0.01
        self.rueda_izq_trasera_joint_current_angle += 0.01
        self.rueda_der_trasera_joint_current_angle += 0.01
        self.aspersor_joint_current_angle += 0.01
        self.angle_msg.data = [self.rueda_izq_delantera_joint_current_angle, self.rueda_der_delantera_joint_current_angle, self.rueda_izq_trasera_joint_current_angle, self.rueda_der_trasera_joint_current_angle, self.aspersor_joint_current_angle]
        self.angle_publisher.publish(self.angle_msg)

def main(args=None):
    rclpy.init(args=args)
    joint_angle_position_publisher_node = JointAnglePositionPublisher()
    try:
        rclpy.spin(joint_angle_position_publisher_node)
    except KeyboardInterrupt:
        joint_angle_position_publisher_node.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()