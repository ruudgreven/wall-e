from time import sleep
import serial

ser = serial.Serial("/dev/serial/by-id/usb-MicroPython_Board_in_FS_mode_e6635c08cb2c3136-if00", parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

#ser.write(("servo:eyebrow_right:0").encode('utf-8'))

ser.write("panic\r".encode())

#for x in range(0,10):
#    sleep(0.25)
#    # ser.write(("servo:eyebrow_right:" + str(x)).encode('utf-8'))
#    ser.write(("servo:eyebrow_right:60").encode('utf-8'))
#    sleep(0.25)
#    # ser.write(("servo:eyebrow_right:" + str(x)).encode('utf-8'))
#    ser.write(("servo:eyebrow_right:0").encode('utf-8'))