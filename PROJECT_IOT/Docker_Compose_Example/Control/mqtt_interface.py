# look for services in SC
import paho.mqtt.client as mqtt
import time
import json
import requests
import service_search
from threading import *
from registration import *
from on_message_callback import *

import string2numpy as s2n


# url = service_search.search('http://localhost:8082','mqtt-broker-at-localhost')


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

        dummy = json.loads(msg.payload.decode('utf-8'))
        print((f'This is dummy...\n{dummy}'))

        # the received message will have the following structure.
        # {
        # "bn":"basename",
        # "e":{"n":"name","t":time","v","value"}
        # }
        dict_handler(self,dummy)


        # # dummy =(msg.payload.decode('utf-8'))
        # if dummy['resource_name'] == 'motion01':
        #     self.mypub('home/led01', dummy['motion'])
        # else:
        #     # self.mypub('home/led01', dummy['push_button'])
        #     if dummy['push_button']==True:
        #         requests.get('http://raspberrypi:8091/')
        #         time.sleep(5)

        # self.mymessage = json.loads(msg.payload.decode('utf-8'))
        # Mqtt subs states
        # create a file that stores the latest state of the system
        # self.mypub()#error
        # print(self.mymessage)
        # with open(self.mymessage['resource_name']+'.json','w') as file:
        #      json.dump(self.mymessage,file)
        #      print(f'{self.mymessage["resource_name"]} is updated')

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
    def __init__(self,id):
        # initialize an instance of an MQTT client as well
        print('controller instance created...')
        with open('initialization.json', 'r') as file:
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
                    # print(self.active_resources_list)
                    for R in self.active_resources_list:
                        if R['type'] == 'MQTT_2sub2':
                            self.rc_sub_namelist.append(R['resource_name'])
                            self.rc_sub_topiclist.append(R['topic'])
                        if R['type'] == 'MQTT_2pub2':
                            self.rc_pub_namelist.append(R['resource_name'])
                            self.rc_pub_topiclist.append(R['topic'])

                    print(f'to sub to name list{self.rc_sub_namelist} topic list {self.rc_sub_topiclist}')
                    print(f'to pub to name list{self.rc_pub_namelist} topic list {self.rc_pub_topiclist}')


        except:
            print('could not update resources')

    def sub_to_RCs(self):
        try:
            self.update_resources_list()
            #print(self.active_resources_list)
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
            a_a.update_resources_list()
            a_a.sub_to_RCs()
            time.sleep(5)

mythread2 = controller_thread('idd')
mythread2.start()
mythread2.join()