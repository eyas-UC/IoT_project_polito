import serial

ser = serial.Serial(port = 'com0com',baudrate=115200)  # open first serial port
print (ser.portstr )      # check which port was really used
ser.write("hello")      # write a string
msg = ser.read(port ='com0com',baudrate=115200) #read the content of the input buffer until you get 100 byte or a timeout event
print(msg) #print the content you might need to decode it print(decode(msg))
ser.close()