# Made by Timodrien 2025

import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# I2C und PCA9685 initialisieren
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Servos definieren
servos = {
    0: servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500), #Head
    1: servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2500), #Neck

    2: servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2500), #Shoulder rotate
    3: servo.Servo(pca.channels[3], min_pulse=500, max_pulse=2500), #Shoulder to side
    4: servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2500), #Elbow
    5: servo.Servo(pca.channels[5], min_pulse=500, max_pulse=2500), #Hand rotate

    6: servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2500), #Shoulder rotate - Right
    7: servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2500), #Shoulder to side - Right
    8: servo.Servo(pca.channels[8], min_pulse=500, max_pulse=2500), #Elbow - Right
    9: servo.Servo(pca.channels[9], min_pulse=500, max_pulse=2500), #Hand rotate - Right
}

servos[0].angle = 90
servos[1].angle = 90

servos[2].angle = 90
servos[3].angle = 0
servos[4].angle = 0
servos[5].angle = 90

servos[6].angle = 90
servos[7].angle = 180
servos[8].angle = 180
servos[9].angle = 90

# Letzter Befehl zur Duplikat-Erkennung
last_command = ""

async def handle_servo_command(command):
    global last_command
    if command != last_command:
        last_command = command
        if command.startswith("S"):
            try:
                colon_index = command.index(":")
                servo_num = int(command[1:colon_index])
                angle = int(command[colon_index + 1:])
                if 1 <= servo_num <= 10 and 0 <= angle <= 180:
                    servos[servo_num - 1].angle = angle
                    #print(f"[Servo] Moved Servo {servo_num} to {angle}°")
            except Exception as e:
                print(f"[Servo Error] {e}")