import requests
import numpy as np

def string2numpy(data):

	string = data.decode('utf-8') #start decoding the string
	suint8tring = string.replace('[', '')
	suint8tring = suint8tring.replace(']', '')
	
	my_array = np.squeeze(np.fromstring(suint8tring, sep=',', count=60000, dtype=np.uint8)) #COUNT 6000, I AM NOT SURE ABOUT THAT, CV2 USES STANDARD RESOLUTIONS
	my_array = np.reshape(my_array, (-1, 300))  # becomes 2dims (second dim is here)

	strr = np.array_str(my_array)
	#print(hashlib.md5(strr.encode('utf-8')).hexdigest())
	#print(my_array.shape)

	return my_array