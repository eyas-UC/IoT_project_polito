import json
import requests
import time
from service_search import *


def registration(json_file, url,id=None):
    # Import informations and metadata from haar.json
    obj = json.load(open(json_file))

    while True:
        try:
            services_list = (search(url))
            # print(services_list)
            for S in services_list:
                if S['id'] == id:
                    print('no need to post')
            else:
                print('ok')
                x = requests.post(url, json.dumps(obj))
                x = x.json()
                # print(x.text)
                ID = x['id']
                print(f'id is {ID}')
                print('registration succedeed\nID is {}'.format(ID))
            while True:
                try:
                    x = requests.put(url + ID, json.dumps(obj))
                    ID = json.loads(x.text)['id']
                    print('update succeeded\nID is {}'.format(ID))
                    time.sleep(5)
                except:
                    print('update failed with the host')

        except:
            print('registration failed with the host')
        time.sleep(5)
