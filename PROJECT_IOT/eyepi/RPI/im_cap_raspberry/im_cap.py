import picamera
import time
import cv2
import cherrypy
import time
import requests
import numpy as np
import sys
import hashlib
import json
from registration import *
from threading import *

# url = 'http://localhost:8082/'
class HelloWorld(object):
    exposed = True

    def GET(self):
        np.set_printoptions(threshold=sys.maxsize) 
        print('catpturing image')
        try:
            # allow the camera to warmup
            time.sleep(0.1)
            # capture frames from the camera
            with picamera.PiCamera() as camera:
                camera.resolution = (320, 240)
                camera.framerate = 24
                time.sleep(0.2)
                output = np.empty((240, 320, 3), dtype=np.uint8)
                camera.capture(output, 'rgb')
                print(output.shape)
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                
                gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)                    # cv2.imshow('frame',frame)
                dsize = (300,200)                 
                gray = cv2.resize(gray, dsize)
                print(gray.shape)
                        # print('safe02') 
                strrr=np.array_str(gray) 
                        # print('safe03')
                        # print(strrr) 
                print(hashlib.md5(strrr.encode('utf-8')).hexdigest())                  
                        # print(strrr)
                full_length = gray.shape[0]*gray.shape[1]
                        # print(f'full_length is {full_length}\n')
                d1_mat = np.squeeze(np.reshape(gray,(1,full_length)))
                str_array=np.array2string(d1_mat, separator=',',precision=4,suppress_small=False)
                        # print(hashlib.md5(str_array.encode('utf-8')).hexdigest())
                        # print('safe')
                #print(str_array)
                return str_array
        except:
            print('something went wrong')
            webcam.release()
            return ('something went wrong caputure ')
        
class  rc_registration_thread(Thread):
    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        while True:
            time.sleep(1)
            try:
                url ="http://192.168.1.151:8087/"
                registration('im_cap.json', url,'camera01')
            except:
                print('error in registration')


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.tree.mount(HelloWorld(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    # cherrypy.config.update({'server.socket_host': 'localhost'})
    
    cherrypy.config.update({'server.socket_port': 8091})
    cherrypy.engine.start()
    url = 'http://192.168.1.151:8087/'  # in the host
    a = rc_registration_thread(1)
    a.start()
    a.join()
    
    
