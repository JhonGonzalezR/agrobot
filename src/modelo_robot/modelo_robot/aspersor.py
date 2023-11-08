import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

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
        if msg.data == "move_180":
            self.move_180_degrees()

    def move_180_degrees(self):
        steps = 200  # Cantidad de pasos para una rotación completa
        delay = 0.005  # Ajusta esto para controlar la velocidad del motor

        # Gira 180 grados hacia la izquierda
        GPIO.output(self.DIR_PIN, -1)  # Cambia la dirección
        for _ in range(steps):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            rclpy.sleep(delay)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            rclpy.sleep(delay)

        rclpy.sleep(1.0)  # Pausa de 1 segundo

        # Gira 180 grados hacia la derecha
        GPIO.output(self.DIR_PIN, 1)  # Cambia la dirección de nuevo
        for _ in range(steps):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            rclpy.sleep(delay)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            rclpy.sleep(delay)

def main(args=None):
    rclpy.init(args=args)
    node = StepperMotorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
