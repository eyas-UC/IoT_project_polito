import numpy as np
import cv2 
import sys
import requests
import json
import cherrypy
import registration as reg
import string2numpy as s2n
from service_search import *
from resource_search import *
import threading

class HaarREST(object):
	exposed = True
	def __init__(self):
		pass

	def GET(self,**params):
		print(params.values())
		return 'sorry bae'
		#uri ,
		print('im here  there')

		if self.found == True:
			try:
				face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
				np.set_printoptions(threshold=sys.maxsize)
				cam = "http://"+self.cameral_url+":"+self.cameral_port
				# print('url is this \n\n'+cam)
				data = requests.get(cam).content #retrieving data from im_cap.py [string]
				my_array = s2n.string2numpy(data)
				# print(my_array)
				# show image
				# cv2.imshow('Color image', my_array)
				# cv2.waitKey(5000)
				# cv2.destroyAllWindows()

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
		else :
			self.__init__()
			return('try again')

	def POST(self):
		cam_url = cherrypy.request.body.read().decode('utf-8')
		try:
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
			np.set_printoptions(threshold=sys.maxsize)
			data = requests.get(cam_url).content #retrieving data from im_cap.py [string]
			my_array = s2n.string2numpy(data)

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




class  cherry_thread(threading.Thread):
	def __init__(self, thread_ID):
		threading.Thread.__init__(self)
		self.thread_ID = thread_ID

	def run(self):
		Haar = HaarREST()
		conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
		cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8098})
		cherrypy.tree.mount(Haar, '/', conf)
		cherrypy.engine.start()

class sc_registration_thread(threading.Thread):

	def __init__(self, thread_ID):
		threading.Thread.__init__(self)
		self.thread_ID = thread_ID
		with open('initialization.json') as file:
			self.dicto = json.load(file)
		# print(dict)
		file.close()
	def run(self):
		# registering and updating of the registration
		# url = 'http://linksmart:8082/'  # when using a docker container
		try:
			url = self.dicto['sc_url']
			reg.registration('haar.json', url, 'haar')

		except:
			print('error trying local')
			# url = self.dicto['sc_url_local']
			# reg.registration('haar.json', url, 'haar')

if __name__ == '__main__':
    a2 = sc_registration_thread(2)
    a3 = cherry_thread(3)
    a2.start()
    a3.start()
    a2.join()
    a3.join()