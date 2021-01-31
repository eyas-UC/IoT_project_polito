import json
import requests
import time
from service_search import *


def registration(json_file, url,id=None):
    # Import informations and metadata from haar.json
    obj = json.load(open(json_file))
    # print('id is {}'.format(id))

    while True:
        try:
            #get all services from url (of linksmart)
            services_list = search(url)
            # print(services_list)
            for S in services_list:
                sid = S['apis'][0]['id']
                # print(f'sid is {sid}')
                if sid == id:

                    # print('no need to post')
                    print('U succedeed')
                    requests.put(url, json.dumps(obj))
                    time.sleep(5)
                    break

            else:
                requests.post(url, json.dumps(obj))
                print('R succedeed')
                time.sleep(5)
        except:
            print('error in registration')