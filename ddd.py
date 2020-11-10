import time
import serial
import numpy as np

random_no = np.random.uniform(0,1,(4096,1))
mylist = (random_no.tolist())
print(random_no.shape)
mystr = str(mylist)
# print(mystr)
mystr = mystr.replace('[', '')
mystr = mystr.replace(']', '')
mystr = mystr.replace(',', '')

# configure the serial connections (the parameters differs on the device you are connecting to)
com = 'COM7'
ser = serial.Serial(port=com, baudrate=128000 , parity=serial.PARITY_NONE , stopbits=serial.STOPBITS_ONE)

state = ser.isOpen()

print(f'{state}\nStarting serial transmission on {com} ')

while True:
    # mystr='0.12345678'
# for n in [1]:
    mystr = '    0.1234567 0.9876543 0.2135798 0.1234567 0.9876543 0.2135798 0.1234567 0.9876543 0.2135798 0.1234567'
    ser.write((mystr.encode()))
    time.sleep(0.3)
    print(mystr)
    print(len(mystr))
