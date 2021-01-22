import requests
import time


if __name__ == '__main__':
	print('hello there')
	# url = 'http://255.255.255.255:8080'
	url = 'http://appb:8080/'
	while True:
		try:
			r = requests.get(url).text
			#print('succeeded')
		except:
			#print('failed')
		time.sleep(1)