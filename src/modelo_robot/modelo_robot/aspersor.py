import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import time

class aspersor(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("aspersor") # MODIFY NAME
        self.suscriber_ = self.create_subscription(Joy,"joy",self.callbackJoyPressed,10)
        self.get_logger().info("Leyendo valores de Joystick")

        # Define las conexiones del motor paso a paso y pasos por revolución:
        self.dirPin = 27  # Puedes ajustar los números de los pines según tu configuración
        self.stepPin = 22
        self.stepsPerRevolution = 200
        self.bombaPin = 25 # Pin para la bomba

        # Configura la biblioteca RPi.GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dirPin, GPIO.OUT)
        GPIO.setup(self.stepPin, GPIO.OUT)
        GPIO.setup(self.bombaPin, GPIO.OUT)



    def callbackJoyPressed(self,msg):
        if msg.buttons[2] == 1:
            self.rotar()
        


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
            self.step_motor(GPIO.HIGH, 5 * self.stepsPerRevolution, 500)
            self.aspersar()
            time.sleep(1)

            # Gira el motor 5 revoluciones rápidamente en sentido antihorario
            self.step_motor(GPIO.LOW, 5 * self.stepsPerRevolution, 500)
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
