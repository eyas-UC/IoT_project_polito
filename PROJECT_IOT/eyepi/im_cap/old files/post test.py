import json
import time
import requests
url = 'http://localhost:8082/'   

myobj = """{
			  "type": "post_test",
			  "title": "post_test",
			  "description": "put_put",
			  "meta": {},
			  "apis": [
			    {
			      "id": "2",
			      "title": "3",
			      "description": "string", 
			      "protocol": "string",
			      "url": "localhost:8090",
			      "spec": {
			        "mediaType": "string",
			        "url": "string",
			        "schema": {}
			      },
			      "meta": {}
			    }
			  ],
			  "doc": "string",
			  "ttl": 3
			}"""

try:
    x = requests.post(url,myobj)
    print(x.text)
    id=json.loads(x.text)["id"]
    print('registration succeeded\nID is {}'.format(id))

except:
    print('registration failed with the host')

while True:
	x = requests.put(url+id,myobj)
	id=json.loads(x.text)["id"]
	print('update succeeded\nID is {}'.format(id))
	time.sleep(5)
