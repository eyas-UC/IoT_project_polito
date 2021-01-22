import cherrypy
import cv2
import time
import requests
import numpy as np
import sys
import hashlib
import registration as reg


class HelloWorld(object):
    exposed = True

    def GET(self):
        webcam = cv2.VideoCapture(0 )
        print('catpturing image')
        try:
            while (webcam.isOpened()):
                ret, frame = webcam.read()
                if ret == True:
                    # diplay all the array without ...
                    np.set_printoptions(threshold=sys.maxsize)
                    #convert to grayscale (reduce size by 3)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                    # cv2.imshow('frame',frame)
                    dsize = (64,64)
                    gray = cv2.resize(gray, dsize)
                    print('safe02')
                    # grey = grey.reshape(grey.shape)
                    gray = gray.reshape(gray.shape[0], -1).T
                    gray = (gray)*(1/255)
                    strrr=np.array_str(gray)
                    print(gray)
                    print('safe03')
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
    cherrypy.config.update({'server.socket_port': 8088})
    cherrypy.engine.start()
    cherrypy.engine.block()


    # url = 'http://linksmart:8082/' #when using docker container
    url = 'http://localhost:8087/' # in the host
    #reg.registration('im_cap.json',url)

    

    cherrypy.engine.exit()


    