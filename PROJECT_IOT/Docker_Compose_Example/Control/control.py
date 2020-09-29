#periodically check if someone pushed door bell the camera periodic GET to camera
#periodically check door-bell (push-button) (subscribe to device connector of push button)
# if Harr says that there is a face notify the owner of an existance of a face.

##### I think we should use multi threading for each task




###  getting data
# look for services in SC
import json
import requests
import service_search
from threading import *
from registration import *


url = service_search.search('http://localhost:8082','mqtt-broker-at-localhost')

class Controller:
    def __init__(self):
        with open('initialization.json', 'r') as file:
            dict = json.load(file)
        file.close()
        #check if the right service catalog is up
        try:
            if requests.get(dict['sc_url']).status_code == 200:
                print('the service catalog is up and running')
        except:
            print('the service catalog is down')

    def get_data(self):
        pass

    def action(self):
        pass

    def user_interface(self):
        pass








a_a = Controller()

