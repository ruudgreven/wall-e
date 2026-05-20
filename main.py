from flask import Flask
from flask import render_template

import serial

global ser
ser = serial.Serial("/dev/serial/by-id/usb-MicroPython_Board_in_FS_mode_e6635c08cb2c3136-if00", parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

app = Flask(__name__)

@app.route("/")
def render_website():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.post('/drive/<direction>')
def drive(direction):
    global ser
    if (direction=="forward"):
        ser.write(("motor:both:forward:40\r").encode())
        return {'drive': 'forward'}
    
    if (direction=="backward"):
        ser.write(("motor:both:backward:40\r").encode())
        return {'drive': 'backward'}

@app.post('/turn/<direction>')
def turn(direction):
    global ser
    if (direction=="left"):
        ser.write(("motor:left:backward:40\r").encode())
        ser.write(("motor:right:forward:40\r").encode())
        return {'turn': 'left'}
    
    if (direction=="right"):
        ser.write(("motor:left:forward:40\r").encode())
        ser.write(("motor:right:backward:40\r").encode())
        return {'turn': 'right'}

@app.post('/stop')
def stop():    
    global ser
    ser.write(("motor:both:stop:0\r").encode())
    return {'stop': 'stop'}

if __name__ == '__main__':
    app.run(debug=True)

#ser.write(("panic").encode())

# Drive forward
#ser.write(("motor:both:forward:40\r").encode())
#sleep(3)
#ser.write(("motor:both:backward:20\r").encode())
#sleep(3)
#ser.write(("motor:both:stop:0\r").encode())

#sleep(1)
#ser.write(("servo:head_rotation:60:3000\r").encode())
#sleep(4)
#ser.write(("servo:head_rotation:120:3000\r").encode())
#sleep(4)


#ser.write(("servo:neck_top:0:3000\r").encode())
#sleep(4)
#ser.write(("servo:neck_top:170:3000\r").encode())
#sleep(4)

#ser.write(("servo:neck_bottom:0:3000\r").encode())
#sleep(4)
#ser.write(("servo:neck_bottom:150:3000\r").encode())
#sleep(4)

#ser.write(("servo:eyes:0:3000\r").encode())
#sleep(4)
#ser.write(("servo:eyes:35:3000\r").encode())
#sleep(4)

#ser.write(("servo:eyebrows:0\r").encode())
#sleep(2)
#ser.write(("servo:eyesbrows:80\r").encode())
#sleep(2)

#ser.write(("servo:arm_left:0:3000\r").encode())
#ser.write(("servo:arm_left:0:3000\r").encode())
#sleep(4)
#ser.write(("servo:arm_left:35:3000\r").encode())
#ser.write(("servo:arm_left:0:3000\r").encode())
#sleep(4)


#ser.write("panic\r".encode())

#for x in range(0,10):
#    sleep(0.25)
#    # ser.write(("servo:eyebrow_right:" + str(x)).encode('utf-8'))
#    ser.write(("servo:eyebrow_right:60").encode('utf-8'))
#    sleep(0.25)
#    # ser.write(("servo:eyebrow_right:" + str(x)).encode('utf-8'))
#    ser.write(("servo:eyebrow_right:0").encode('utf-8'))