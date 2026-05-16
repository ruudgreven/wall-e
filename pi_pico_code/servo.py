# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-servo-motor-micropython/

from machine import Pin, PWM
import time

class Servo:
    __servo_pwm_freq = 50
    __min_u16_duty = 1639
    __max_u16_duty = 8192
    min_angle = 0
    max_angle = 180
    current_angle = 0
     
    pin = -1
    begin_limit = 0
    end_limit = 180
    reverse = False
    
    animation_startangle = 0
    animation_endangle = 0
    animation_starttime = -1
    animation_endtime = -1

    def __init__(self, pin, min_u16_duty, max_u16_duty, begin_limit, end_limit, reverse):
        self.update_settings(self.__servo_pwm_freq, min_u16_duty, max_u16_duty, 0, 180, pin)
        self.begin_limit = begin_limit
        self.end_limit = end_limit
        self.reverse = reverse

    def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u16_duty = min_u16_duty
        self.__max_u16_duty = max_u16_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)

    def setLimits(self, begin_limit, end_limit):
        self.begin_limit = begin_limit;
        self.end_limit = end_limit;

    def move(self, angle):
        # If animating to a certain angle stop the action
        if (self.animation_endtime >= 0):
            self.animation_starttime = -1
            self.animation_endtime = -1
            self.animation_startangle = 0
            self.animation_endangle = 0
            
        # Normalize angle
        angle = round(angle, 2)
        if (self.reverse):
            angle = self.end_limit - angle
        
        if (angle > self.end_limit):
            angle = self.end_limit
        if (angle < self.begin_limit):
            angle = self.begin_limit
        
        # do we need to move?
        if angle == self.current_angle:
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self.__angle_to_u16_duty(angle)
        self.__motor.duty_u16(duty_u16)
    
    def moveToCenter(self):
        self.move((self.end_limit - self.begin_limit) / 2 + self.begin_limit)
    
    def startAnimation(self, angle, duration):
        angle = round(angle, 2)
        
        # Normalize angle
        if (self.reverse):
            angle = self.end_limit - angle
        if (angle > self.end_limit):
            angle = self.end_limit
        if (angle < self.begin_limit):
            angle = self.begin_limit
        
        if (self.reverse):
            self.animation_startangle = self.end_limit - self.current_angle
            self.animation_endangle = self.end_limit - angle
        else:
            self.animation_startangle = self.current_angle
            self.animation_endangle = angle

        self.animation_starttime = time.ticks_us()
        self.animation_endtime = time.ticks_us() + (duration * 1000)
        
    def animate(self):
        if (time.ticks_us() <= self.animation_endtime):
            #self.current_angle = angle
            currentTime = time.ticks_us() - self.animation_starttime
            duration = (self.animation_endtime - self.animation_starttime)
            angle = (self.animation_endangle - self.animation_startangle) * (currentTime / duration) + self.animation_startangle

            # Normalize angle
            angle = round(angle, 2)
            if (self.reverse):
                angle = self.end_limit - angle
            
            if (angle > self.end_limit):
                angle = self.end_limit
            if (angle < self.begin_limit):
                angle = self.begin_limit
            
            if angle == self.current_angle:
                return
            self.current_angle = angle
            
            duty_u16 = self.__angle_to_u16_duty(angle)
            self.__motor.duty_u16(duty_u16)
        else:
            self.animation_starttime = -1
            self.animation_endtime = -1
            self.animation_startangle = 0
            self.animation_endangle = 0
            
    def stop(self):
        self.__motor.deinit()
    
    def get_current_angle(self):
        return self.current_angle

    def __angle_to_u16_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty


    def __initialise(self, pin):
        self.current_angle = -0.001
        self.pin = pin
        self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)
