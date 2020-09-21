import numpy as np
import cv2 
import time
import sys
import hashlib
import requests
import json
import cherrypy

class HaarREST(object):
	exposed = True
	def __init__(self):
		pass

	def GET(self):
		try:
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
			np.set_printoptions(threshold=sys.maxsize)
			data = requests.get('http://127.1.1.2:8088').content #retrieving data from im_cap.py [string]
			string = data.decode('utf-8') #start decoding the string
			string = data.decode('utf-8')
			suint8tring = string.replace('[', '')
			suint8tring = suint8tring.replace(']', '')
		
			my_array = np.squeeze(np.fromstring(suint8tring, sep=',', count=60000, dtype=np.uint8)) #COUNT 6000, I AM NOT SURE ABOUT THAT, CV2 USES STANDARD RESOLUTIONS
			my_array = np.reshape(my_array, (-1, 300))  # becomes 2dims (second dim is here)

			strr = np.array_str(my_array)
			#print(hashlib.md5(strr.encode('utf-8')).hexdigest())
			#print(my_array.shape)

			try:
				faces = face_cascade.detectMultiScale(my_array, 1.3, 5)
				if len(faces) > 0: #looking at how many faces are detected
					detected_faces = True
				else:
					detected_faces = False

			except:
				raise cherrypy.HTTPError(500, 'Impossible to use Haar Functions')

			output = {'Face':detected_faces, 'Number of detected faces':len(faces)}

			return json.dumps(output)

		except:
			raise cherrypy.HTTPError(500, 'Impossible to process the Image')



if __name__ == '__main__':


	Haar = HaarREST()
	conf = {
		'/':{
				'request.dispatch':cherrypy.dispatch.MethodDispatcher()
				#'tool.session.on':True
		}
	}

	cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port':85})
	cherrypy.tree.mount(Haar, '/', conf)
	cherrypy.engine.start()
	#cherrypy.engine.exit()
