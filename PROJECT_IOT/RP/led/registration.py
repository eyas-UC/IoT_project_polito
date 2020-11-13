import json
import requests
import time



def registration(json_file, url,resource_name):
    # Import informations and metadata from haar.json
    with open(json_file,'r') as file:
        obj = json.load(file)
    file.close()
    #print('ok here')
    while True:
        try:
            list_a = requests.get(url).json()['list_of_RCs']
            time.sleep(3.5)
            found = False
            for R in list_a:
                if R['resource_name'] == resource_name:
                    requests.put(url,json.dumps(obj))
                    #time.sleep(3)
                    print('U succeeded')
                    found = True                
            if found == False:
                print('not found')
                requests.post(url, json.dumps(obj) )
                print('R succedeed')
        except:
            print('regisration failed with the host')
