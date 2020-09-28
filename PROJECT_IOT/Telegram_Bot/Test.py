import telepot
import urllib.request
import requests
import numpy as np
import cv2
import time
import json
import string2numpy as s2n

def on_chat_message(msg):
	#content_type, chat_type, chat_id = telepot.glance(msg)
	#if content_type == 'text':
	#	name = msg["from"]["first_name"]
	#	txt = msg['text']
	#	print(msg)
	#furl=urllib.request.urlopen('http://127.1.1.2:8080.jpg')
	chat_id=-1001168249039
	data = requests.get('http://127.1.1.2:8090').content
	my_array=s2n.string2numpy(data)
	cv2.imwrite('capture.jpg',my_array)

	bot.sendPhoto(chat_id, open('capture.jpg','rb'))
	

if __name__ == '__main__':


	url = 'http://linksmart:8082/'

	TOKEN= '1398161201:AAFQv0YyeLqAaFdiegs3qnXs9R6wTppdHEg'

	reg.registration('Telegram_bot.txt',url)

	bot = telepot.Bot(TOKEN)
	msg="picture"
	on_chat_message(msg)
	#bot.message_loop(on_chat_message)
	print ('Listening ...')



	time.sleep(5)

