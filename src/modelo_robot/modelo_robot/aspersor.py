import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
import time

class aspersor(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("aspersor") # MODIFY NAME
        self.suscriber_ = self.create_subscription(Int64,"activation",self.activate,10)
        self.get_logger().info("Leyendo valores de Joystick")

        # Define las conexiones del motor paso a paso y pasos por revolución:
        self.dirPin = 5  # Puedes ajustar los números de los pines según tu configuración
        self.stepPin = 6
        self.stepsPerRevolution = 200
        self.bombaPin = 26 # Pin para la bomba

        # Configura la biblioteca RPi.GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dirPin, GPIO.OUT)
        GPIO.setup(self.stepPin, GPIO.OUT)
        GPIO.setup(self.bombaPin, GPIO.OUT)



    def activate(self,msg):
        if msg.data == 1:
            self.get_logger().info("Rotando")
            self.rotar()
        else:
            self.get_logger().info("Rotación detenida")
        


    def step_motor(self,direction, steps, delay_us):
        # Establece la dirección del giro
        GPIO.output(self.dirPin, direction)

        # Gira el motor el número especificado de pasos
        for _ in range(steps):
            GPIO.output(self.stepPin, GPIO.HIGH)
            time.sleep(delay_us / 1000000.0)
            GPIO.output(self.stepPin, GPIO.LOW)
            time.sleep(delay_us / 1000000.0)

    def aspersar(self):
        GPIO.output(self.bombaPin, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.bombaPin, GPIO.LOW)

    def rotar(self):
        try:
        
            # Gira el motor 5 revoluciones rápidamente en sentido horario
            self.step_motor(GPIO.HIGH, 1 * self.stepsPerRevolution, 5000)
            self.aspersar()
            time.sleep(1)

            # Gira el motor 5 revoluciones rápidamente en sentido antihorario
            self.step_motor(GPIO.LOW, 1 * self.stepsPerRevolution, 5000)
            self.aspersar()
            time.sleep(1)

        except KeyboardInterrupt:
            # Detén el motor y limpia la configuración de GPIO cuando se interrumpe el programa con Ctrl+C
            GPIO.cleanup()


def main(args=None):
    rclpy.init(args=args)
    node = aspersor() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()