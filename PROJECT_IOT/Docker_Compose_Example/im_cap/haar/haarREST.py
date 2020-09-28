import numpy as np
import cv2 
import sys
import requests
import json
import cherrypy
import registration as reg
import string2numpy as s2n

class HaarREST(object):
	exposed = True
	def __init__(self):
		pass

	def GET(self):
		try:
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
			np.set_printoptions(threshold=sys.maxsize)
			
			data = requests.get('http://127.1.1.2:8088').content #retrieving data from im_cap.py [string]
			
			my_array = s2n.string2numpy(data)

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
		}
	}

	cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port':8098})
	cherrypy.tree.mount(Haar, '/', conf)
	cherrypy.engine.start()

	#url = 'http://linksmart:8082/'
	url = 'http://localhost:8087/'

	reg.registration('haar.json', url)






	#cherrypy.engine.exit()
