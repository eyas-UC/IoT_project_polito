# periodically check if someone pushed door bell the camera periodic GET to camera
# periodically check door-bell (push-button) (subscribe to device connector of push button)
# if Harr says that there is a face notify the owner of an existance of a face.
# periodically register itself

##### I think we should use multi threading for each task


###  getting data
# look for services in SC
import paho.mqtt.client as mqtt
import time
import json
import requests
import service_search
from threading import *
from registration import *
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
        print('you received: ' + msg.payload.decode('utf-8'))
        self.mymessage = json.loads(msg.payload.decode('utf-8'))
        with open('motion01.json','w') as file:
            json.dump(self.mymessage,file)
            file.close()
        # log
        print(f'{self.mymessage["resource_name"]} is updated')

        #print(type(self.mymessage))

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
        print('msg is published')

    def stop(self):

        if (self.isSubscriber):
            self.mqtt_client.unsubscribe(self.topic)

        self.mqtt_client.loop_stop()
        print('loop stopped')
        self.mqtt_client.disconnect()
        print('disconnect gracefully')





class Controller:
    def __init__(self):
        # initialize an instance of an MQTT client as well
        with open('initialization.json', 'r') as file:
            dict = json.load(file)
        file.close()
        # check if the right service catalog is up
        self.service_catalog_url = dict['sc_url']
        self.broker = dict['broker']
        self.port = dict['port']
        self.sc_response = requests.get(dict['sc_url'])
        self.mqtt_instance = client('id_02',self.broker,self.port)
        self.mqtt_instance.start()
        self.mqtt_instance.isSubscriber = False
        self.mqtt_instance.mymessage=''


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
            self.get_ser_urls() # update active services list (default port of linksmart is 8082)
            # print(self.active_services_list) # for debugging
            for S in self.active_services_list:

                if S['title'] == 'RC':# look for resource catalog in service catalog
                    #there should be only one instance of RC running at a time
                    url = S['apis'][0]['url']
                    x = requests.get(url).json()
                    self.active_resources_list = x["list_of_RCs"]
                    self.rc_sub_namelist =[]
                    self.rc_sub_topiclist=[]
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


                    # print(self.rc_sub_namelist)
                    # print(self.rc_sub_topiclist)
        except:
            print('could not update resources')

    def sub_to_RCs(self):
        try:
            self.update_resources_list()
            for topic in self.rc_sub_topiclist:
                print(f'topic is {topic}')
                self.mqtt_instance.mySub(topic)
        except:
            print('could not subscribe')

class  logic(Thread):

    def __init__(self, thread_ID):
        Thread.__init__(self)

    def run(self):
        # a_a = Controller()
        # a_a.sub_to_RCs()
        while True:
            time.sleep(0.1)
            # print(((a_a.mqtt_instance.mymessage)))
            print(a_a.mqtt_instance.mymessage)


class  controller_thread(Thread):

    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        time.sleep(3)



a_a = Controller()
a_a.sub_to_RCs()

mythread2 = controller_thread('idd')
mythread2.start()
mythread2.join()
mythread = logic('idd')
mythread.start()
mythread.join()

