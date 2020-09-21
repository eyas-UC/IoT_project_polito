import numpy as np
import cv2
import time
import sys
import hashlib
import requests



face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
np.set_printoptions(threshold=sys.maxsize)

while True:
	try:
		print('capturing image')
		detected_face = False
		#get data from im_cap.py
		data = requests.get('http://127.1.1.2:8080').content
		# content of that get request is a string. Now we have to translate this string into 2D numpy array
		string = data.decode('utf-8')
		suint8tring = string.replace('[', '')
		suint8tring = suint8tring.replace(']', '')
		#print(suint8tring)		
		my_array = np.squeeze(np.fromstring(suint8tring, sep=',', count=60000, dtype=np.uint8)) #COUNT 6000, I AM NOT SURE ABOUT THAT, CV2 USES STANDARD RESOLUTIONS
		my_array = np.reshape(my_array, (-1, 300))  # becomes 2dims (second dim is here)
		#print(my_array)
		strr = np.array_str(my_array)
		print(hashlib.md5(strr.encode('utf-8')).hexdigest())
		print(my_array.shape)

		#print(my_array)

		#now that we have the matrix, we can use haar to detect faces.
		try:	
			faces = face_cascade.detectMultiScale(my_array, 1.3, 5)
			
			if faces.shape[0]>0: #looking at how many faces are detected
				detected_face = True
				print('Face detected')
		except:
			print('No face detected')

		print(face_detected)



	except:
		print('OPS!!!\nsomething went wrong!!!')
		# return 'OPS!!!\nsomething went wrong!!!'

