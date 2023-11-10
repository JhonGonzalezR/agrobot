#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from example_interfaces.msg import Int64




class joy_activator(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("joy_activator") # MODIFY NAME

        self.cont = 0
        self.suscriber_ = self.create_subscription(Joy,"joy",self.callbackJoyPressed,10)
        self.get_logger().info("Se ha suscribido a /joy")

        self.publisher_ = self.create_publisher(Int64, "activation", 10)

        self.publish_timer_ = self.create_timer(1.0, self.public_count)

        

    def callbackJoyPressed(self,msg):
        if msg.buttons[2] == 1:
            self.cont += 1

        if self.cont == 2:
            self.cont = 0

    def public_count(self):
        msg2 = Int64()
        msg2.data = self.cont
        self.publisher_.publish(msg2)



def main(args=None):
    rclpy.init(args=args)
    node = joy_activator() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()