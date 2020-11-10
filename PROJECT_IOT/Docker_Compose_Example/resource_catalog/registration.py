import json
import requests
import time
from service_search import *


def registration(json_file, url,id=None):
    # Import informations and metadata from haar.json
    obj = json.load(open(json_file))

    while True:
        try:

            services_list = search(url)
            # print(id)
            # print("list is \n\n \n",services_list)
            # print(services_list[0]['apis'][0]['id'])
            for S in services_list:
                if S['apis'][0]['id'] == id:
                    print('no need to post')
                    time.sleep(2)
            else:
                # print('ok')
                x = requests.post(url, json.dumps(obj))
                x = x.json()
                # print(x.text)
                # ID = x['id']
                # print(f'id is {ID}')
                print('registration succedeed')
                time.sleep(2)

            while True:
                try:
                    requests.put(url, json.dumps(obj))

                    print('update succeeded')
                    time.sleep(3)
                except:
                    print('update failed with the host')
                    time.sleep(2)


        except:
            print('registration failed with the host')
        time.sleep(3)
