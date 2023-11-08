#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time
from sensor_msgs.msg import Joy



class aspersor(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("aspersor") # MODIFY NAME
        self.suscriber_ = self.create_subscription(Joy,"joy",self.callbackJoyPressed,10)
        self.get_logger().info("Leyendo valores de Joystick")

        self.DIR_PIN = 19  # Pin para la dirección del motor (Dir)
        self.STEP_PIN = 20  # Pin para el pulso del motor    (STEP)
        self.bombaPin = 25 # Pin para la bomba

        self.start = 0
        Joy.buttons
        

        # Configurar los pines GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        GPIO.setup(self.bombaPin, GPIO.OUT)


        
    def callbackJoyPressed(self,msg):
        if msg.buttons[2] == 1:
            self.start += 1
            self.get_logger().info("Boton presionado")
        if self.start == 2:
            self.start = 0
        self.rotarMotor()


    def aspersar(self):
        GPIO.output(self.bombaPin, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.bombaPin, GPIO.LOW)

    def rotarMotor(self):
        try:
            

            if self.start == 1:

                # Gira 180 grados hacia la derecha
                GPIO.output(self.DIR_PIN, GPIO.HIGH)         # Establecer la dirección del motor hacia la derecha
                for i in range(200):                    # 200->180° y 100->90°
                    GPIO.output(self.STEP_PIN, GPIO.HIGH)
                    time.sleep(0.1)                   # Controla la velocidad
                    GPIO.output(self.STEP_PIN, GPIO.LOW)
                    time.sleep(0.1)                   # Controla la velocidad
                    self.aspersar()

                # Gira 180 grados hacia la izquierda
                GPIO.output(self.DIR_PIN, GPIO.LOW)         # Establecer la dirección del motor hacia la izquierda
                for i in range(200):                   # 200->180° y 100->90°
                    GPIO.output(self.STEP_PIN, GPIO.HIGH)
                    time.sleep(0.1)                  # Controla la velocidad
                    GPIO.output(self.STEP_PIN, GPIO.LOW)
                    time.sleep(0.1)                  # Controla la velocidad
                    self.aspersar()
                         

        except KeyboardInterrupt:
            pass




def main(args=None):
    rclpy.init(args=args)
    node = aspersor() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()