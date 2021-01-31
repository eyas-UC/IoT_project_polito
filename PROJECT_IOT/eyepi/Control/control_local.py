import paho.mqtt.client as mqtt
import time
import json
import requests
import service_search
import threading
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

# event handler function is a function inside the message callback of the MQTT
# it checks the sensor name,no, and house no, then decide where what action
#  should be taken accordingly
def event_handler(self, dicto=None):

    # message structure
    # bn => house no
    # e  => event dictionary
    # n  => name of sensor
    # {
    # "bn":"xx",
    # "e":{"n":"motion", "no":"number","t":time","v","value"}
    # }
    house_no = dicto['bn']
    sen_name = dicto['e']['n']
    sen_no = dicto['e']['no']
    updated_time = dicto['e']['t']
    value = dicto['e']['v']

    # conditions here
    ##########################################

    if sen_name == 'motion':
        # pub message to led
        if value == True:
            # response to motion in the house
            try:
                dump_dict = {'e': {'v': True, 'time': str(time.time())}}
                # turn ON the LED using mqtt message
                self.mypub('home' + house_no + '/led' + sen_no, json.dumps(dump_dict))
                # look for the bot and get its url
                # print(self.service_catalog_url)
                state, boturl = service_search.search(sc_url="http://localhost:8082/" ,service_title='bot')
                # telegram here
                if state == True:
                # if state is true --> bot RESTAPI is working
                    full_url = boturl + '/motion'
                    print(full_url)
                    requests.post(full_url, (json.dumps(dicto)))  #send POST request to telegram bot API
                # send post request to some service that translate post to bot messages
                # log this data
            except:
                print('error in dictionary1')

        if value == False:
            try:
                # turn OFF the LED using mqtt message
                push_dict = {'e': {'v': False, 'time': str(time.time())}}
                self.mypub('home' + house_no + '/led' + sen_no, json.dumps(push_dict))
            except:
                print('error in dictionary')
            # print('False')


    if sen_name == 'push_button':
        try:
            push_dict = {'e': {'v': True, 'time': str(time.time())}}
            # print('push button state is changed')
            if value == True:
                print('push_button pressed')
                # look for botREST api
                state, boturl = service_search.search(sc_url="http://localhost:8082/" ,service_title='bot')
                ####################################
                # Sending telegram POST request here
                if state == True:
                #state is true when the API is active
                    full_url = boturl + '/push_button'
                    requests.post(full_url, (json.dumps(dicto)))



                for dump_dict in self.rc_REST_dict_list:
                    if dump_dict['house_ID'] == house_no:
                        # cam found in the same house where pb is pressed
                        state, haar_url = service_search.search(sc_url="http://localhost:8082/",service_title='Haar')
                        print(haar_url)

                        if state == True:
                            cam_url = 'http://' + dump_dict["URL"] + ':' + dump_dict["port"]
                            print(cam_url)
                            # haar accepts a post request with the link of the camera's address
                            x = requests.post(haar_url, cam_url)
                            print(x.json())
                            # send result of face detection to bot
                            full_url = boturl + '/haar'
                            dicto['e']['v'] = x.json()
                            dicto['e']['n'] = 'haar'
                            requests.post(full_url, json.dumps(dicto))
        except:
            print('error pushbutton posting/haar')


# mqtt client class (generic except for)
# on message calls event handler

class client():
    def __init__(self, clientID, broker, port):
        self.clientID = clientID
        self.broker = broker
        self.port = port
        # print('broker={},port={}'.format(broker, port))
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
        # print('controller instance created...')
        with open('initialization.json') as file:
            dict = json.load(file)
        # print(dict)
        file.close()
        # check if the right service catalog is up
        self.service_catalog_url = dict['sc_url']
        self.broker = dict['broker']#raspberry pi broker is used in this case
        self.port = dict['port']

        # in this section of code
        # we try to connect to the dockerized then local host if not dockerized
        try:
            self.service_catalog_url = dict['sc_url']
            self.sc_response = requests.get(dict['sc_url'])
        except:
            print('trying to connect to service catalog\nusing local address')
            try:
                self.service_catalog_url =dict['sc_url_local']
                self.sc_response = requests.get(dict['sc_url_local'])
            except:
                self.__init__(id)
        # print(self.sc_response)
        self.mqtt_instance = client(id, self.broker, self.port)
        try:
            self.mqtt_instance.start()

        except:
            print('unable to connect to MQTT broker check raspberrypi')
        self.mqtt_instance.isSubscriber = False
        try:
            if self.sc_response.status_code == 200:
                print('the service catalog is up and running')
                # proceed later on with the registration of control
        except:
            print('the service catalog is down')

    def get_ser_urls(self):
        # get the current active service lists
        # print(self.service_catalog_url)

        self.active_services_list = service_search.search("http://localhost:8082/")
        # print(self.active_services_list)

    # this method will update several variables (list of resources names and list of their topics)
    # MQTT resources  to subscribe to / to publish to
    # REST resources

    def update_resources_list(self):
        # the resources should include motion sensor, camera, LED, and push button
        # updates the self.active_resources_list
        try:
            self.get_ser_urls()  # update active services list (default port of linksmart is 8082)
            # print(self.active_services_list) # for debugging
            for S in self.active_services_list:
                # print(S)

                if S['title'] == 'RC':  # look for resource catalog in service catalog
                    print(S['title'])
                    # there should be only one instance of RC running at a time
                    # url = S['apis'][0]['url'] #docker
                    url = S['doc']#localhost
                    # print(url)
                    x = requests.get(url).json()
                    # print(x)
                    self.active_resources_list = x["list_of_RCs"]
                    print(self.active_resources_list)
                    self.rc_sub_namelist = []
                    self.rc_sub_topiclist = []
                    self.rc_pub_namelist = []
                    self.rc_pub_topiclist = []
                    self.mqtt_instance.rc_REST_dict_list = []
                    for R in self.active_resources_list:
                        if R['type'] == 'MQTT_2sub2':
                            self.rc_sub_namelist.append(R['resource_name'])
                            self.rc_sub_topiclist.append(R['topic'])
                        if R['type'] == 'MQTT_2pub2':
                            self.rc_pub_namelist.append(R['resource_name'])
                            self.rc_pub_topiclist.append(R['topic'])
                        if R['type'] == 'REST':
                            self.mqtt_instance.rc_REST_dict_list.append(R)

                    # print(f'to sub to name list{self.rc_sub_namelist} topic list {self.rc_sub_topiclist}')
                    # print(f'to pub to name list{self.rc_pub_namelist} topic list {self.rc_pub_topiclist}')
                    # print(f'added {self.mqtt_instance.rc_REST_dict_list}')
        except:
            print('could not update resources or no resources')

    # subscribe to all topics of active
    def sub_to_RCs(self):
        try:
            self.update_resources_list()
            # print(self.active_resources_list)
            for topic in self.rc_sub_topiclist:
                # print(f'topic is {topic}')
                self.mqtt_instance.mySub(topic)
        except:
            print('could not subscribe')



class sc_registration_thread(threading.Thread):

    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
        with open('initialization.json') as file:
            self.dicto = json.load(file)
        # print(dict)
        file.close()

    def run(self):
        # registering and updating of the registration

        # url = 'http://linksmart:8082/'  # when using a docker container
        try:
            url =  self.dicto['sc_url']
            registration('Control_REST.json', url, 'control')
        except:
            print('error in trying local')
            # url = self.dicto['sc_url_local']
            # registration('Control_REST.json', url, 'control')



class controller_thread(threading.Thread):

    def __init__(self, thread_ID):
        threading.Thread.__init__(self)

    def run(self):
        # controlling led
        a_a = Controller('1')
        while True:
            # subscribe to resources every 30 secs
            # maybe a new resource is up now
            a_a.sub_to_RCs()
            time.sleep(30)


mythread2 = controller_thread('idd')
mythread1 = sc_registration_thread('registration')
mythread1.start()
mythread2.start()
mythread1.join()
mythread2.join()
