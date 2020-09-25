import telepot
import urllib.request
import requests
import numpy as np
import cv2
import time

def on_chat_message(msg):
	#content_type, chat_type, chat_id = telepot.glance(msg)
	#if content_type == 'text':
	#	name = msg["from"]["first_name"]
	#	txt = msg['text']
	#	print(msg)
	#furl=urllib.request.urlopen('http://127.1.1.2:8080.jpg')
	chat_id=806699255
	data = requests.get('http://127.1.1.2:8090').content
	string = data.decode('utf-8')
	suint8tring = string.replace('[', '')
	suint8tring = suint8tring.replace(']', '')
	my_array = np.squeeze(np.fromstring(suint8tring, sep=',', count=60000, dtype=np.uint8))
	my_array = np.reshape(my_array, (-1, 300))  # becomes 2dims (second dim is here)
	strr = np.array_str(my_array)
	cv2.imwrite('capture.jpg',my_array)

	bot.sendPhoto(chat_id, open('capture.jpg','rb'))
	
		#bot.sendMessage(chat_id, 'ciao %s, sono un bot di Mirko!'%name)
		#bot.sendMessage(chat_id, 'ho ricevuto questo: %s'%txt)

if __name__ == '__main__':
	myobj = """{
              "type": "service",
              "title": "Telegram_bot",
              "description": "put_put",
              "meta": {},
              "apis": [
                {
                  "id": "2",
                  "title": "3",
                  "description": "string", 
                  "protocol": "string",
                  "url": "localhost:8090",
                  "spec": {
                    "mediaType": "string",
                    "url": "string",
                    "schema": {}
                  },
                  "meta": {}
                }
              ],
              "doc": "string",
              "ttl": 3
            }"""

	url = 'http://linksmart:8082/'

	TOKEN= '1398161201:AAFQv0YyeLqAaFdiegs3qnXs9R6wTppdHEg'


	while 1:
		try:
			x = requests.post(url, myobj)
			ID = json.loads(x.text)['id']
			print(f'id is {ID}')
			print('registration succeeded\nID is {}'.format(ID))
			while True:
				try:
					x = requests.put(url + ID, myobj)
					ID = json.loads(x.text)['id']
					print('update succeeded\nID is {}'.format(ID))
					time.sleep(5)

				except:
					print('update failed with the host')
					time.sleep(5)


		except:
			print('registration failed with the host')
			time.sleep(5)

		bot = telepot.Bot(TOKEN)
		msg="picture"
		on_chat_message(msg)
		#bot.message_loop(on_chat_message)
		print ('Listening ...')



		time.sleep(5)

