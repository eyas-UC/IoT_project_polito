import cherrypy
import cv2
import time
import requests
import numpy as np
import sys

class HelloWorld(object):
    exposed = True

    def GET(self):
    	array =np.zeros((1,10))
    	
    	str_array=np.array2string(array, precision=4, separator=',',suppress_small=True)
    	# str_array =np.array_str(array)
    	return str_array


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
    cherrypy.engine.block()