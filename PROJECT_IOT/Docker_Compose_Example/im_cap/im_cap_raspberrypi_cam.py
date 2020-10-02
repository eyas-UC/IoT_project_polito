from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import cherrypy
import time
import requests
import numpy as np
import sys
import hashlib
import json
myobj = """{
              "type": "REST_API",
              "title": "image_capture",
              "description": "image capture",
              "meta": {},
              "apis": [
                {
                  "id": "4",
                  "title": "im_cap",
                  "description": "string", 
                  "protocol": "string",
                  "url": "localhost:8088",
                  "spec": {
                    "mediaType": "string",
                    "url": "string",
                    "schema": {}
                  },
                  "meta": {}
                }
              ],
              "doc": "string",
              "ttl": 3
            }"""

url = 'http://linksmart:8082/'


# url = 'http://localhost:8082/'
class HelloWorld(object):
    exposed = True

    def GET(self):
        webcam = cv2.VideoCapture(0 )
        np.set_printoptions(threshold=sys.maxsize) 
        print('catpturing image')
        try:
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.framerate = 32
            rawCapture = PiRGBArray(camera, size=(640, 480))
            # allow the camera to warmup
            time.sleep(0.1)
            # capture frames from the camera
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
                image = frame.array
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                    # cv2.imshow('frame',frame)
                dsize = (300,200)                 
                gray = cv2.resize(gray, dsize)
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
                webcam.release()
                print(str_array)
                return str_array
        except:
            print('something went wrong')
            webcam.release()
            return ('something went wrong caputure ')
        webcam.release()


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
    url = 'http://localhost:8087/'  # in the host
    reg.registration('im_cap.json', url)