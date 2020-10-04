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
        with open('initialization.json', 'r') as file:
            dict = json.load(file)
        file.close()
        # check if the right service catalog is up
        self.service_catalog_url = dict['sc_url']
        self.sc_response = requests.get(dict['sc_url'])
        try:
            if self.sc_response.status_code == 200:
                print('the service catalog is up and running')
                # proceed later on with the registration of control
        except:
            print('the service catalog is down')

    def get_ser_urls(self):

        self.active_services_list = service_search.search(self.service_catalog_url)
        print(self.active_services_list)

    def update_resources(self):
        # the resources should include motion sensor, camera, LED, and push button
        # updates the self.active_resources_list
        try:
            self.get_ser_urls() # update active services list
            # print(self.active_services_list) # for debugging
            for S in self.active_services_list:
                #
                if S['title'] == 'RC':# look for resource catalog in service catalog
                    url = S['apis'][0]['url']
                    x = requests.get(url).json()
                    self.active_resources_list = x["list_of_RCs"]
                    # print(f'list of the active resources {self.active_resources_list}')
        except:
            print('could not update resources')

        # for S in self.active_services_list:
        #     if S['apis'][0]['protocol'] == 'MQTT':
        #         self.sub
        #         pass
        # self.haar_output = requests.get()

    def logic(self):
        pass

    def action(self):
        pass

    def user_interface(self):
        pass



# if __name__ == '__main__':
#     broker = 'test.mosquitto.org'
#     broker_port = 1883
#     sensor_id = 'id_2'
#     sensor1 = client(sensor_id, broker, broker_port)
#     sensor1.start()
#

a_a = Controller()
a_a.update_resources()
print('\n\n\n\n')
print(a_a.active_resources_list)

