#periodically check if someone pushed door bell the camera periodic GET to camera
#periodically check door-bell (push-button) (subscribe to device connector of push button)
# if Harr says that there is a face notify the owner of an existance of a face.
# periodically register itself

##### I think we should use multi threading for each task




###  getting data
# look for services in SC
import json
import requests
import service_search
from threading import *
from registration import *
import string2numpy as s2n


# url = service_search.search('http://localhost:8082','mqtt-broker-at-localhost')

class Controller:
    def __init__(self):
        with open('initialization.json', 'r') as file:
            dict = json.load(file)
        file.close()
        #check if the right service catalog is up
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
        return (self.active_services_list)
    def init_rc(self):
        for S in self.active_services_list:
            if S['id'] == 'RC'
        for S in self.active_services_list:
            if S['apis'][0]['protocol'] == 'MQTT':
                self.sub
                pass
        self.haar_output = requests.get()

    def logic(self):
        # if haar_output
        pass


    def action(self):
        pass

    def user_interface(self):
        pass








a_a = Controller()
