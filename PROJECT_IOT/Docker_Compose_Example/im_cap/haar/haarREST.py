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


class HaarREST(object):
	exposed = True
	def __init__(self):
		self.cameral_url = None
		try:
			print('hello')

			#get list of services
			self.service_list = search('http://localhost:8082')
			# print(self.service_list)
			for S in self.service_list:
				if S['title'] == 'RC':
					print('the resource catalog is working\nfinding the camera...')
					self.resources_list = r_search()
					# print(self.resources_list)
					for R in self.resources_list:
						if R['resource_name'] == 'camera01':
							self.cameral_url = R['URL']
							print('\n\ncamera found at {} \n\n'.format(self.cameral_url))


		except:
			print('cannot connect to linksmart')




	def GET(self):
		print('im here  there')
		# if self.cameral_url == None:
		# 	print('if')
		# 	#self.__init__()# get data from service catalog the from resource catalog
		# 	pass
		# else:
		try:
			print('else')
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
			np.set_printoptions(threshold=sys.maxsize)

			print('im here  there')

			# data = requests.get(self.cameral_url).content #retrieving data from im_cap.py [string]
			data = requests.get("http://192.168.1.150:8091").content #retrieving data from im_cap.py [string]
			my_array = s2n.string2numpy(data)
			print(my_array)

			cv2.imshow('Color image', my_array)
			cv2.waitKey(5000)
			cv2.destroyAllWindows()

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

	# url = 'http://linksmart:8082/'
	url = 'http://localhost:8082/'

	reg.registration('haar.json', url)






	#cherrypy.engine.exit()
