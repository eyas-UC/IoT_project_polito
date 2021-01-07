import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
import requests
import time
import cherrypy
import registration as reg
import threading
import paho.mqtt.client as mqtt
import service_search
import resource_search
import string2numpy as s2n
import cv2
from io import BytesIO
import numpy as np
class RESTBot:
    exposed=True
    def __init__(self, token):
        # Local token
        self.tokenBot = token
        # Catalog token
        # self.tokenBot=requests.get("http://catalogIP/telegram_token").json()["telegramToken"]
        try:
            print('setting up bot')
            self.bot = telepot.Bot(self.tokenBot)
            self.bot.deleteWebhook()
            print('set up complete')
            self.chatIDs=[]
            # initialize an instance of an BOT MQTT client as well
            with open('initialization.json') as file:
                # print('opened file successfully')
                dicto = json.load(file)
                file.close()
                # print(dicto)
                # print(type(dicto))
            # print(f'json file of the initialization {dicto}')

            # print('closed file successfully')
            # print(dicto)

            # check if the right service catalog is up
            self.service_catalog_url = dicto['sc_url']
            self.broker = dicto['broker']
            self.port = dicto['port']

            # self.sc_response = requests.get(self.service_catalog_url)

            # print('the response of Service Catalog'+self.sc_response)
            my_id = 'bot_mqtt'
            # print(self.broker,self.port)

            self.mqtt_instance = client('iidi', self.broker, self.port)
            print('bot mqtt instance created...')
            self.mqtt_instance.start()
            # self.mqtt_instance.isSubscriber = False
            self.mqtt_instance.mymessage = ''
            print('set up complete')
        except:
            print('settup failed    ')
        self.__message={"alert":"","action":""}
        MessageLoop(self.bot, {'chat': self.on_chat_message}).run_as_thread()
    # for messages from the telegram user
    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        self.chatIDs.append(chat_ID)
        message = msg['text']
        if message == "/switchOn":
            payload = self.__message.copy()
            # payload['e']['v'] = "on"
            payload = {'e':{"v":"True"}}
            payload['e']['v'] = True
            payload['e']['time'] = time.time()
            self.mqtt_instance.mypub('home01/led01', json.dumps(payload))
            self.bot.sendMessage(chat_ID, text="Led switched on")
        elif message == "/switchOff":
            payload = self.__message.copy()
            payload = {'e':{"v":False}}
            self.mqtt_instance.mypub('home01/led01', json.dumps(payload))
            self.bot.sendMessage(chat_ID, text="Led switched off")
        elif message =="/start":
            self.bot.sendMessage(chat_ID, text="Welcome")
        elif message == "/faces01":
            state, haar_url = service_search.search(service_title='Haar')
            if state == True:
                state,rc_url=service_search.search(service_title = 'RC')
                # print(state,rc_url)
                RC_list =resource_search.r_search()
                for dicto in RC_list:
                    if dicto['house_ID'] == "home01" and dicto['resource_name'][0:6] == 'camera':
                        pass
                        # print(f'url is {dicto["URL"]} Port is {dicto["port"]}' )
                        cam_url =f'http://{dicto["URL"]}:{dicto["port"]}'
                        print(cam_url)
                        x = requests.post(haar_url, cam_url)
                        print(x.json())
                        self.bot.sendMessage(chat_ID, text=str(x.json()))
        elif message == "/picture01":
                state,rc_url=service_search.search(service_title = 'RC')
                # print(state,rc_url)
                if state == True:
                    RC_list =resource_search.r_search()
                    for dicto in RC_list:
                        if dicto['house_ID'] == "home01" and dicto['resource_name'][0:6] == 'camera':
                            pass
                            # print(f'url is {dicto["URL"]} Port is {dicto["port"]}' )
                            cam_url =f'http://{dicto["URL"]}:{dicto["port"]}'
                            print(cam_url)
                            # self.bot.sendMessage(chat_ID, text=str(x.json()))
                            data = requests.get(cam_url).content  # retrieving data from im_cap.py [string]
                            my_array = s2n.string2numpy(data)
                            cv2.imwrite('buffer_file.jpg', my_array)
                            with open('buffer_file.jpg') as file:
                                # url = f'https://api.telegram.org/bot{self.tokenBot}/sendPhoto'
                                self.bot.sendPhoto(chat_ID, photo=open('buffer_file.jpg', 'rb'))
                                # self.bot
                                file.close()


        else:
            self.bot.sendMessage(chat_ID, text="Command not supported")
# actuation
    def POST(self,*uri):
        tosend=''
        output={"status":"not-sent","message":tosend}
        if len(uri)!=0:
            if uri[0]=='motion':
                body=cherrypy.request.body.read()
                jsonBody=json.loads(body)
                tosend = (jsonBody)
                for chat_ID in self.chatIDs:
                    print(chat_ID)
                    self.bot.sendMessage(chat_ID, text=tosend)
        return json.dumps(output)

class client():
    def __init__(self, clientID, broker, port):
        self.clientID = clientID
        self.broker = broker
        self.port = port
        print('broker={},port={}'.format(broker, port))
        # initializing an instance
        self.mqtt_client = mqtt.Client(clientID)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message_r
        self.mqtt_client.on_log = self.on_log

    def on_log(self, paho_mqtt, usertdata, level, buf):
        # print('log: '+buf)
        pass

    def on_connect(self, paho_mqtt, userdata, flags, rc):
        if rc == 0:
            print('connected to the broker {}'.format(self.broker))

        else:
            print(f'bad connection')

    def on_message_r(self, paho_mqtt, userdata, msg):
        ## write functions that checks conditions
        ## then calls smaller functions that performs the actual MQTT Actions
        ## function should get the name of resource and its number
        ## looking function ---> for all mqtt resources(mqtt 2sub2) and their numbers
        ## get data(done by being in on message function) and do action
        ## the recieved sensor data(json) should contain which house / user / client

        received_dict = json.loads(msg.payload.decode('utf-8'))
        print(received_dict)

    def mySub(self, topic):
        print('subscribing to {}'.format(topic))
        self.mqtt_client.subscribe(topic)
        self.isSubscriber = True
        self.topic = topic

    def start(self):
        self.mqtt_client.connect(self.broker, self.port)
        self.mqtt_client.loop_start()
        print('loop is started')

    def mypub(self, topic, msg):
        # print(topic+' '+ msg)
        self.mqtt_client.publish(topic, msg, 2)
        # print('msg is published')

    def stop(self):

        if (self.isSubscriber):
            self.mqtt_client.unsubscribe(self.topic)

        self.mqtt_client.loop_stop()
        print('loop stopped')
        self.mqtt_client.disconnect()
        print('disconnect gracefully')


class cherry_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        conf = json.load(open("settings.json"))
        token = conf["telegram_token"]
        conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
        bot = RESTBot(token)
        cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8099})
        cherrypy.tree.mount(bot, '/', conf)
        cherrypy.engine.start()
        while 1:
            time.sleep(1)

class  sc_registration_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        # registering and updating of the registration
        # url = 'http://linksmart:8082/'  # when using a docker container
        url = 'http://localhost:8082/'
        reg.registration('bot_REST.json', url,'bot')


if __name__ == "__main__":
    a2 = sc_registration_thread(2)
    a3 = cherry_thread(3)
    a2.start()
    a3.start()
    a2.join()
    a3.join()
