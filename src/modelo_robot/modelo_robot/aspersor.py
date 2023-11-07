import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time

class Nema17ControlNode(Node):
    def __init__(self):
        super().__init__('nema17_control_node')

        self.DEVICE_DIR_PIN = 19
        self.DEVICE_STEP_PIN = 20
        self.DEVICE_PUSH_PIN = 6
        self.get_logger().info("Leyendo valores de Joystick")

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DEVICE_DIR_PIN, GPIO.OUT)
        GPIO.setup(self.DEVICE_STEP_PIN, GPIO.OUT)
        GPIO.setup(self.DEVICE_PUSH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.start_motor = 1

        self.timer_period = 0.001
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        if self.start_motor == 1:
            GPIO.output(self.DEVICE_DIR_PIN, GPIO.HIGH)
            for i in range(200):
                GPIO.output(self.DEVICE_STEP_PIN, GPIO.HIGH)
                time.sleep(self.timer_period)
                GPIO.output(self.DEVICE_STEP_PIN, GPIO.LOW)
                time.sleep(self.timer_period)

            GPIO.output(self.DEVICE_DIR_PIN, GPIO.LOW)
            for i in range(200):
                GPIO.output(self.DEVICE_STEP_PIN, GPIO.HIGH)
                time.sleep(self.timer_period)
                GPIO.output(self.DEVICE_STEP_PIN, GPIO.LOW)
                time.sleep(self.timer_period)

        if not GPIO.input(self.DEVICE_PUSH_PIN):
            self.start_motor = 0
        else:
            self.start_motor = 1

def main(args=None):
    rclpy.init(args=args)
    node = Nema17ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
