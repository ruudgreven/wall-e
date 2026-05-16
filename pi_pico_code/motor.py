from machine import Pin, PWM

class Motor:
    in1 = -1	# Or in3 for the other motor
    in2 = -1	# Or in4 for the other motor
    en = -1		# EN for the motor
    reverse = False
    minPwm = -1
    maxPwm = -1
    
    def __init__(self, in1, in2, en, reverse, minPwm, maxPwm):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.en = PWM(en, freq=1000)
        self.reverse = reverse
        self.minPwm = minPwm
        self.maxPwm = maxPwm
        
    def forward(self):
        if (self.reverse == False):
            self.in1.value(1)
            self.in2.value(0)
        else:
            self.in1.value(0)
            self.in2.value(1)

    def backward(self):
        if (self.reverse == False):
            self.in1.value(0)
            self.in2.value(1)
        else:
            self.in1.value(1)
            self.in2.value(0)
                      
    def stop(self):
        self.in1.value(0)
        self.in2.value(0)

    def setSpeed(self, speed):
        if speed <= 0:
            speed = 0
        if speed > 100:
            speed = 100
     
        duty = ((self.maxPwm - self.minPwm) / 100 * speed) + self.minPwm
        self.en.duty_u16(int(duty))
