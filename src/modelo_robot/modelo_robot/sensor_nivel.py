import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import RPi.GPIO as GPIO
import time

class LEDControl:
    def __init__(self, pin, min_distance, max_distance):
        self.pin = pin
        self.min_distance = min_distance
        self.max_distance = max_distance
        GPIO.output(self.pin, GPIO.LOW)

    def update(self, distance):
        if self.min_distance <= distance <= self.max_distance:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)

class UltrasonicSensorNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_sensor_node')
        
        # Declaración de pines sensor ultrasónico
        self.trigger_pin = 18
        self.echo_pin = 23

        # Declaración de pines para LEDs
        self.led1_pin = 13  # GPIO para el primer LED Rojo
        self.led2_pin = 6  # GPIO para el segundo LED Amarillo
        self.led3_pin = 5  # GPIO para el tercer Verde

        # Definición de entradas y salidas
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.led1_pin, GPIO.OUT)
        GPIO.setup(self.led2_pin, GPIO.OUT)
        GPIO.setup(self.led3_pin, GPIO.OUT)

        # Inicialización de nodos de LEDControl
        self.led1 = LEDControl(self.led1_pin, 0, 10)  # LED1 se enciende a menos de 50 cm
        self.led2 = LEDControl(self.led2_pin, 11, 20)  # LED2 se enciende entre 51 cm y 100 cm
        self.led3 = LEDControl(self.led3_pin, 21, float('inf'))  # LED3 se enciende entre 101 cm y inf cm

        # Publicador para el rango medido
        self.publisher_ = self.create_publisher(Range, 'ultrasonic_range', 10)

        # Temporizador para actualizar la lectura y publicar
        self.timer = self.create_timer(0.5, self.update_and_publish)

    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.0001)
        GPIO.output(self.trigger_pin, False)

    def wait_for_echo(self, value, timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count > 0:
            count = count - 1

    def get_distance(self):
        self.send_trigger_pulse()
        self.wait_for_echo(True, 10000)
        start = time.time()
        self.wait_for_echo(False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        return distance_cm

    def update_and_publish(self):
        cm = self.get_distance()

        # Actualizar el estado de los LEDs
        self.led1.update(cm)
        self.led2.update(cm)
        self.led3.update(cm)

        # Publicar el rango medido
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = 0.1  # Ejemplo de valor; ajustar según las especificaciones reales
        msg.min_range = 0.02  # Ejemplo de valor; ajustar según las especificaciones reales
        msg.max_range = 4.0  # Ejemplo de valor; ajustar según las especificaciones reales
        msg.range = cm / 100.0  # Convertir de cm a metros
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
