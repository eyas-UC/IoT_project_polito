import json
import requests
import time



def registration(json_file, url):
    # Import informations and metadata from haar.json
    obj = json.load(open(json_file))

    while True:
        try:
            print('ok')
            x = requests.post(url, json.dumps(obj))
            print('ok')
            print(x.json())
            print('registration succedeed')
            time.sleep(2)
            while True:
                try:
                    x = requests.put(url, json.dumps(obj) )
                    print('update succeeded')
                    time.sleep(5)
                except:
                    print('update failed with the host')

        except:
            print('registration failed with the host')
        time.sleep(5)
        



