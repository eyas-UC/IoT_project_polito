import paho.mqtt.client as mqtt
import time
import json
import requests
import service_search
from threading import *
from registration import *
import telepot
from telepot.loop import MessageLoop

import string2numpy as s2n


def number_handler(bn):
    word_list = bn.split('/')
    number = ''
    for char in word_list[0]:
        if char.isdigit():
            number += char
    if number == '':
        return 'wrong format'
    else:
        return (number)


def event_handler(self, dicto = None):
    # {
    # "bn":"homexx/sensors",
    # "e":{"n":"motion", "no":"number","t":time","v","value"}
    # }
    basename = dicto['bn']
    house_no = number_handler(basename)
    sen_name = dicto['e']['n']
    sen_no = dicto['e']['no']
    updated_time = dicto['e']['t']
    value = dicto['e']['v']
    # conditions here
    ##########################################

    if sen_name == 'motion':
        # pub message to led
        print(sen_no)
        if value == True:
            print('True')
            print('house no is ' + house_no)
            try:
                push_dict = {'e': {'v': True, 'time': str(time.time())}}

                self.mypub('home' + house_no + '/led' + sen_no, json.dumps(push_dict))
                service_search.search('REST_control')
                requests.post('')
                # telegram here
                # send post request to some service that translate post to bot messages
                # log this data
            except:
                print('error in dictionary1')
        if value == False:
            try:
                # pass
                push_dict = {'e': {'v': False, 'time': str(time.time())}}
                self.mypub('home' + house_no + '/led' + sen_no, json.dumps(push_dict))
                # log this data
            except:
                print('error in dictionary')
            print('False')

    if sen_name == 'push_button':
        # print('push button state is changed')
        print(self.rc_REST_dict_list)
        if value == True:
            state, haar_url = service_search.search(service_title='Haar')
            for dicto in self.rc_REST_dict_list:
                if dicto['house_ID'] == "home" + house_no:
                    print(f'house no {house_no} ip {dicto["URL"]} port {dicto["port"]}')
                    cam_url = 'http://' + dicto["URL"] + ':' + dicto["port"]
                    print(f'cam url {cam_url}')
                    print(f'haar url {haar_url}')
                    x = requests.post(haar_url, cam_url)
                    # print(x)
        #     state,url = service_search.search(service_title='Haar')
        #     cam_index = self.rc_REST_namelist.index('camera01')
        #     print(self.rc_REST_urllist[cam_index])
        #     if state == True:
        #         x = requests.post(url,self.rc_REST_urllist[cam_index]).json()
        #         print(x)


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
        event_handler(self, received_dict)

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


class Controller:
    def __init__(self, id):
        # initialize an instance of an MQTT client as well
        print('controller instance created...')
        with open('initialization.json') as file:
            dict = json.load(file)
        print(dict)
        file.close()
        # check if the right service catalog is up
        self.service_catalog_url = dict['sc_url']
        self.broker = dict['broker']
        self.port = dict['port']
        self.sc_response = requests.get(dict['sc_url'])
        print(self.sc_response)
        self.mqtt_instance = client(id, self.broker, self.port)
        self.mqtt_instance.start()
        self.mqtt_instance.isSubscriber = False
        self.mqtt_instance.mymessage = ''

        self.bot = telepot.Bot(self.tokenBot)
        self.bot.deleteWebhook()
        print('set up complete')
        self.chatIDs = []

        try:
            if self.sc_response.status_code == 200:
                print('the service catalog is up and running')
                # proceed later on with the registration of control
        except:
            print('the service catalog is down')

    def get_ser_urls(self):
        # get the current active service lists
        self.active_services_list = service_search.search(self.service_catalog_url)

    def update_resources_list(self):
        # the resources should include motion sensor, camera, LED, and push button
        # updates the self.active_resources_list
        try:
            self.get_ser_urls()  # update active services list (default port of linksmart is 8082)
            # print(self.active_services_list) # for debugging
            for S in self.active_services_list:
                # print(S)

                if S['title'] == 'RC':  # look for resource catalog in service catalog
                    # there should be only one instance of RC running at a time
                    url = S['apis'][0]['url']
                    x = requests.get(url).json()
                    self.active_resources_list = x["list_of_RCs"]
                    self.rc_sub_namelist = []
                    self.rc_sub_topiclist = []
                    self.rc_pub_namelist = []
                    self.rc_pub_topiclist = []
                    self.mqtt_instance.rc_REST_dict_list = []

                    # print(self.active_resources_list)
                    for R in self.active_resources_list:
                        if R['type'] == 'MQTT_2sub2':
                            self.rc_sub_namelist.append(R['resource_name'])
                            self.rc_sub_topiclist.append(R['topic'])
                        if R['type'] == 'MQTT_2pub2':
                            self.rc_pub_namelist.append(R['resource_name'])
                            self.rc_pub_topiclist.append(R['topic'])
                        if R['type'] == 'REST':
                            self.mqtt_instance.rc_REST_dict_list.append(R)

                    print(f'to sub to name list{self.rc_sub_namelist} topic list {self.rc_sub_topiclist}')
                    print(f'to pub to name list{self.rc_pub_namelist} topic list {self.rc_pub_topiclist}')
                    print(f'added {self.mqtt_instance.rc_REST_dict_list}')


        except:
            print('could not update resources')

    def sub_to_RCs(self):
        try:
            self.update_resources_list()
            # print(self.active_resources_list)
            for topic in self.rc_sub_topiclist:
                print(f'topic is {topic}')
                self.mqtt_instance.mySub(topic)
        except:
            print('could not subscribe')


class logic(Thread):

    def __init__(self, thread_ID):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(5)
            # print(((a_a.mqtt_instance.mymessage)))
            # print(a_a.mqtt_instance.mymessage)


class controller_thread(Thread):

    def __init__(self, thread_ID):
        Thread.__init__(self)

    def run(self):
        # controlling led
        a_a = Controller('1')
        while True:
            # a_a.update_resources_list()
            a_a.sub_to_RCs()
            time.sleep(30)


mythread2 = controller_thread('idd')
mythread2.start()
mythread2.join()
