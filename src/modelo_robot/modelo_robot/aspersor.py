import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class StepperMotorNode(Node):

    def __init__(self):
        super().__init__('stepper_motor_node')
        self.publisher_ = self.create_publisher(String, 'stepper_motor_control', 10)
        self.subscription = self.create_subscription(String, 'stepper_motor_command', self.callback, 10)
        self.subscription

        GPIO.setmode(GPIO.BCM)
        self.DIR_PIN = 19  # Pin para la dirección (DIR)
        self.STEP_PIN = 20  # Pin para el pulso (STEP)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        self.direction = 1  # 1 para un sentido, -1 para el contrario

    def callback(self, msg):
        if msg.data == "forward":
            self.direction = 1
        elif msg.data == "backward":
            self.direction = -1

        self.move_motor()

    def move_motor(self):
        steps = 200
        delay = 0.005

        GPIO.output(self.DIR_PIN, self.direction)
        for _ in range(steps):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            time.sleep(delay)  # Utiliza time.sleep() en lugar de rclpy.sleep()
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            time.sleep(delay)  # Utiliza time.sleep() en lugar de rclpy.sleep()

def main(args=None):
    rclpy.init(args=args)
    node = StepperMotorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
