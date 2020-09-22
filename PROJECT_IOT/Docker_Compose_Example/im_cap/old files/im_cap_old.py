import cherrypy
import cv2
import time
import requests
import numpy as np
import sys
import hashlib

myobj = """{
              "type": "post_test",
              "title": "post_test",
              "description": "put_put",
              "meta": {},
              "apis": [
                {
                  "id": "2",
                  "title": "3",
                  "description": "string", 
                  "protocol": "string",
                  "url": "localhost:8090",
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
        webcam = cv2.VideoCapture(0)
        print('catpturing image')
        try:
            while (webcam.isOpened()):
                ret, frame = webcam.read()
                if ret == True:
                    # print(frame.shape)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                    # cv2.imshow('frame',frame)
                    # print(frame.shape)
                    dsize = (160,100)                    
                    gray = cv2.resize(gray, dsize)

                    # print(gray.shape)
                    np.set_printoptions(threshold=sys.maxsize)
                    # print(gray)
                    # str_array=np.array2string(gray, precision=4, separator='-',suppress_small=False)
                    # str_array = np.array_str(gray)
                    # send it as 1d array then retrieve it from the other side as 1d array then use 
                    # np.reshape(1darray,(-1,new_dimesion))
                    
                    full_length = gray.shape[0]*gray.shape[1]
                    print(f'full_length is {full_length}')
                    d1_mat = np.squeeze(np.reshape(gray,(1,full_length)))
                    # str_array=np.array2string(d1_mat, precision=4,suppress_small=False)
                    print(d1_mat.shape)
                    print('safe1')

                    str_array=np.array2string(d1_mat, separator=',',precision=4,suppress_small=False)
                    

                    # str_array = np.array_str(d1_mat)
                    # print(str_array)
                    
                    print(hashlib.md5(str_array.encode('utf-8')).hexdigest())
                    print('safe')
                    webcam.release()
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
    
    cherrypy.config.update({'server.socket_port': 8090})
    cherrypy.engine.start()
    while True:
        try:
            x = requests.post(url, myobj)
            ID = json.loads(x.text)['id']
            print(f'id is {ID}')
            print('registration succeeded\nID is {}'.format(ID))
            while True:
                try:
                    x = requests.put(url + ID, myobj)
                    ID = json.loads(x.text)['id']
                    print('update succeeded\nID is {}'.format(ID))
                    time.sleep(5)

                except:
                    print('update failed with the host')

        except:
            print('registration failed with the host')

    cherrypy.engine.exit()


    