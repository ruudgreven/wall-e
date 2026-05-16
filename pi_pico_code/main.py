from servo import Servo
from motor import Motor
from sys import stdin, stdout
from time import sleep
from machine import Pin,UART,PWM,Timer
import select
import time

HEAD_ROTATION = 0
NECK_TOP = 1
NECK_BOTTOM = 2
EYE_LEFT = 3
EYE_RIGHT = 4
ARM_LEFT = 5
ARM_RIGHT = 6
EYEBROW_LEFT = 7
EYEBROW_RIGHT = 8

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(stdin, select.POLLIN)

# Add Servos (id, Servo(port, min_duty, max_duty, begin_limit, end_limit))
servos = []
servos.insert(HEAD_ROTATION, Servo(15, 1639, 8192, 60, 120, False))	# Head turns max 60 degrees. 60 is look right, 120 is look left
servos.insert(NECK_TOP, Servo(14, 1639, 8192, 0, 170, False))		# Neck turns max 170 degrees. 0 is neck down, 170 is high
servos.insert(NECK_BOTTOM, Servo(13, 1639, 8192, 0, 150,False))
servos.insert(EYE_LEFT, Servo(12, 1639, 8192, 0, 40, False))
servos.insert(EYE_RIGHT, Servo(11, 1639, 8192, 0, 40, True))		
servos.insert(ARM_LEFT, Servo(10, 1639, 8192, 0, 110, True))		# Arm turns max 110 degrees. 0 is arms down. 110 is arm up
servos.insert(ARM_RIGHT, Servo(9, 1639, 8192, 0, 110, False))		# Arm turns max 110 degrees. 0 is arms down. 110 is arm up
servos.insert(EYEBROW_LEFT, Servo(8, 1800, 8000, 0, 80, True))
servos.insert(EYEBROW_RIGHT, Servo(7, 1800, 8000, 0, 80, False))

# Add motors
motorLeft = Motor(Pin(18), Pin(19), Pin(16), False, 25000,45000)
motorRight = Motor(Pin(20), Pin(21), Pin(17), True, 51000, 71000)

def resetAll():
    motorLeft.stop()
    motorRight.stop()
    for servo in servos:
        if (servo.pin == HEAD_ROTATION):
            servo.move(90)
        else:
            servo.move(0)
    
def rotateServo(servo, angle):
    servo.move(angle)

def animateServo(servo, angle, duration):
    servo.startAnimation(angle,duration)

try:
    resetAll()

    print("Start listening")
    
    while True:
        # Animate when needed
        for servo in servos:
            servo.animate()
        
        try:
            poll_results = poll_obj.poll(1) # Wait 1 microsecond
            # Receive data
            if poll_results:
                received_data = stdin.readline().rstrip()
                message = received_data
                if (message==""):
                    continue
                
                # Value input:
                
                command = message.split(":")

                action = command[0]
                
                if (action=="panic"):
                    resetAll();
                    stdout.write("ok:stopped all\r\n")

                # servo:<servo_name>:angle, moves the servo immediatly to the given angle
                elif (action=="servo" and len(command)==3):
                    servoname = command[1]
                    angle = float(command[2])
                
                    if (servoname=="head_rotation"):
                        rotateServo(servos[HEAD_ROTATION],angle)
                        stdout.write("ok:head_rotation\r\n")
                        
                    elif (servoname=="neck_top"):
                        rotateServo(servos[NECK_TOP],angle)
                        stdout.write("ok:neck_top\r\n")
                        
                    elif (servoname=="neck_bottom"):
                        rotateServo(servos[NECK_BOTTOM],angle)
                        stdout.write("ok:neck_bottom\r\n")
                        
                    elif (servoname=="eye_left"):
                        rotateServo(servos[EYE_LEFT],angle)
                        stdout.write("ok:eye_left\r\n")
                        
                    elif (servoname=="eye_right"):
                        rotateServo(servos[EYE_RIGHT],angle)
                        stdout.write("ok:eye_right\r\n")
                    
                    elif (servoname=="eyes"):
                        rotateServo(servos[EYE_LEFT],angle)
                        rotateServo(servos[EYE_RIGHT],angle)
                        stdout.write("ok:eye_left\r\n")
                        stdout.write("ok:eye_right\r\n")
                        
                    elif (servoname=="arm_left"):
                        rotateServo(servos[ARM_LEFT],angle)
                        stdout.write("ok:arm_left\r\n")
                        
                    elif (servoname=="arm_right"):
                        rotateServo(servos[ARM_RIGHT],angle)
                        stdout.write("ok:arm_right\r\n")

                    elif (servoname=="eyebrow_left"):
                        rotateServo(servos[EYEBROW_LEFT],angle)
                        stdout.write("ok:eyebrow_left\r\n")

                    elif (servoname=="eyebrow_right"):
                        rotateServo(servos[EYEBROW_RIGHT],angle)
                        stdout.write("ok:eyebrow_right\r\n")
                        
                # servo:<servo_name>:angle:duration, give the servo a future time
                elif (action=="servo" and len(command)==4):
                    servoname = command[1]
                    angle = float(command[2])
                    duration = float(command[3])
                    
                    if (servoname=="head_rotation"):
                        animateServo(servos[HEAD_ROTATION],angle, duratiom)
                        stdout.write("ok:head_rotation\r\n")
                    
                    elif (servoname=="neck_top"):
                        animateServo(servos[NECK_TOP],angle, duration)
                        stdout.write("ok:neck_top\r\n")
                        
                    elif (servoname=="neck_bottom"):
                        animateServo(servos[NECK_BOTTOM],angle, duration)
                        stdout.write("ok:neck_bottom\r\n")
                        
                    elif (servoname=="eye_left"):
                        animateServo(servos[EYE_LEFT],angle, duration)
                        stdout.write("ok:eye_left\r\n")
                        
                    elif (servoname=="eye_right"):
                        animateServo(servos[EYE_RIGHT],angle, duration)
                        stdout.write("ok:eye_right\r\n")   
                    
                    elif (servoname=="arm_left"):
                        animateServo(servos[ARM_LEFT],angle, duration)
                        stdout.write("ok:arm_left\r\n")
                    
                    elif (servoname=="arm_right"):
                        animateServo(servos[ARM_RIGHT],angle, duration)
                        stdout.write("ok:arm_right\r\n")

                    elif (servoname=="eyebrow_left"):
                        animateServo(servos[EYEBROW_LEFT],angle, duration)
                        stdout.write("ok:eyebrow_left\r\n")

                    elif (servoname=="eyebrow_right"):
                        animateServo(servos[EYEBROW_RIGHT],angle, duration)
                        stdout.write("ok:eyebrow_right\r\n")
                        
                elif (action=="motor" and len(command)==4):
                    motorname = command[1]
                    direction = command[2]
                    speed = float(command[3])
                    
                    if (motorname=="left" or motorname=="both"):
                        if (direction=="forward"):
                            motorLeft.forward()
                            stdout.write("ok:motor left forward")
                        elif (direction=="backward"):
                            motorLeft.backward()
                            stdout.write("ok:motor left backward")
                        elif (direction=="stop"):
                            motorLeft.stop()
                            stdout.write("ok:motor left stop")
                        motorLeft.setSpeed(speed)
    
                    if (motorname=="right" or motorname=="both"):
                        if (direction=="forward"):
                            motorRight.forward()
                            stdout.write("ok:motor right forward")
                        elif (direction=="backward"):
                            motorRight.backward()
                            stdout.write("ok:motor right backward")
                        elif (direction=="stop"):
                            motorRight.stop()
                            stdout.write("ok:motor right stop")
                        motorRight.setSpeed(speed)
                        
                else:
                    stdout.write("error:unknown action\r\n")

        except Exception as error:
            stdout.write("error:exception thrown:" + repr(error) + "\r\n")
            resetAll();
            sleep(1)
        
except KeyboardInterrupt:
    print("Keyboard interrupt\r\n")
    motorLeft.stop()
    motorRight.stop()
    

