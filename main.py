from time import sleep
import serial

ser = serial.Serial("/dev/serial0", baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

ser.write(("servo:eyebrow_right:0").encode('utf-8'))

#for x in range(0,90):
#    sleep(0.05)
#    ser.write(("servo:eyebrow_right:" + str(x)).encode('utf-8'))