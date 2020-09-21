import requests
import time


if __name__ == '__main__':
	url = 'http://localhost:8080'
	while True:
		try:
			r = requests.get(url).text
			print('tried')
		except:
			print('except')
		time.sleep(2)