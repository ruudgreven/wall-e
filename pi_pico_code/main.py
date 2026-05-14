from servo import Servo
from time import sleep
from machine import Pin,UART

HEAD_ROTATION = 0
NECK_TOP = 1
NECK_BOTTOM = 2
EYE_LEFT = 3
EYE_RIGHT = 4
ARM_LEFT = 5
ARM_RIGHT = 6
EYEBROW_LEFT = 7
EYEBROW_RIGHT = 8

# Initialize servos
servos = []

# Pol the serial port
uart = machine.UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))

# Add Servos (id, Servo(port, min_duty, max_duty, begin_limit, end_limit))
servos.insert(HEAD_ROTATION, Servo(0, 1639, 8192, 60, 120, False))	# Head turns max 60 degrees. 60 is look right, 120 is look left
servos.insert(NECK_TOP, Servo(1, 1639, 8192, 0, 170, False))		# Neck turns max 170 degrees. 0 is neck down, 170 is high
servos.insert(NECK_BOTTOM, Servo(2, 1639, 8192, 0, 180,False))
servos.insert(EYE_LEFT, Servo(3, 1639, 8192, 0, 180, False))
servos.insert(EYE_RIGHT, Servo(4, 1639, 8192, 0, 180, True))		
servos.insert(ARM_LEFT, Servo(5, 1639, 8192, 0, 110, True))		# Arm turns max 110 degrees. 0 is arms down. 110 is arm up
servos.insert(ARM_RIGHT, Servo(6, 1639, 8192, 0, 110, False))		# Arm turns max 110 degrees. 0 is arms down. 110 is arm up
servos.insert(EYEBROW_LEFT, Servo(7, 1800, 8000, 0, 80, False))
servos.insert(EYEBROW_RIGHT, Servo(8, 1800, 8000, 0, 80, False))

def resetAll():
    for servo in servos:
        if (servo.pin == HEAD_ROTATION):
            servo.move(90)
        else:
            servo.move(0)
    
def rotateServo(servo, angle):
    servo.move(angle)

try:
    resetAll()
    print("Start listening")
    
    while True:
        try:
            # Receive data
            if uart.any():
                received_data = uart.readline()
                message = received_data.decode('utf-8')
                
                # Value input:
                # servo:<servo_name>:angle
                command = message.split(":")
                if (len(command)==3):            
                    action = command[0]
                    servoname = command[1]
                    angle = float(command[2])
                    
                    if (action=="servo"):
                        if (servoname=="head_rotation"):
                            rotateServo(servos[HEAD_ROTATION],angle)
                            uart.write("ok:head_rotation".encode('utf-8'))
                            
                        if (servoname=="neck_top"):
                            rotateServo(servos[NECK_TOP],angle)
                            uart.write("ok:neck_top")
                            
                        if (servoname=="neck_bottom"):
                            rotateServo(servos[NECK_BOTTOM],angle)
                            uart.write("ok:neck_bottom")
                            
                        if (servoname=="eye_left"):
                            rotateServo(servos[EYE_LEFT],angle)
                            uart.write("ok:eye_left")
                            
                        if (servoname=="eye_right"):
                            rotateServo(servos[EYE_RIGHT],angle)
                            uart.write("ok:eye_right")

                        if (servoname=="arm_left"):
                            rotateServo(servos[ARM_LEFT],angle)
                            uart.write("ok:arm_left")
                            
                        if (servoname=="arm_right"):
                            rotateServo(servos[ARM_RIGHT],angle)
                            uart.write("ok:arm_right")

                        if (servoname=="eyebrow_left"):
                            rotateServo(servos[EYEBROW_LEFT],angle)
                            uart.write("ok:eyebrow_left")

                        if (servoname=="eyebrow_right"):
                            rotateServo(servos[EYEBROW_RIGHT],angle)
                            uart.write("ok:eyebrow_right")
                    
                    else:
                        uart.write("error:unknown action")
                else:
                    uart.write("error:Unknown command")
                    
            sleep(0.05)
        except:
            uart.write("error:exception thrown")
            print("exception thrown")
            sleep(1)
        
except KeyboardInterrupt:
    print("Keyboard interrupt")
    

