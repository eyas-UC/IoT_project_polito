import requests
import time
import numpy as np
import sys
import cv2
import hashlib
import json

np.set_printoptions(threshold=sys.maxsize)
while True:
    try:
        print('capturing image')
        data = requests.get('http://127.1.1.2:8080').content
        string = data.decode('utf-8')
        # print(string)
        # print(hashlib.md5(	string.encode('utf-8')).hexdigest())
        suint8tring = string.replace('[', '')
        suint8tring = suint8tring.replace(']', '')
        # print(suint8tring)
        # my_array =np.fromstring(string, count=-1, sep='')
        my_array = np.squeeze(np.fromstring(suint8tring, sep=',', count=60000, dtype=np.uint8))
        # print((my_array))
        # my_array =np.array( list(string),dtype=int )
        my_array = np.reshape(my_array, (-1, 300))  # becomes 2dims (second dim is here)
        # print('2D ok')
        strr = np.array_str(my_array)
        print(hashlib.md5(strr.encode('utf-8')).hexdigest())
        print(my_array.shape)
        # print(my_array)

        # print((my_array))
        # ndarray = np.full(my_array, 125, dtype=np.uint8)

        # show image
        # print('phase1')
        cv2.imshow('KDDDD', my_array)
        # print(my_array.shape)
          # cv2.waitKey(0) # waits until a key is pressed
        # cv2.destroyAllWindows() # destroys the window showing image
        cv2.waitKey(10)
        # time.sleep(10)

    except:
        print('OPS!!!\nsomething went wrong!!!')
        # return 'OPS!!!\nsomething went wrong!!!'