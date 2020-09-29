#periodically check if someone pushed door bell the camera periodic GET to camera
#periodically check door-bell (push-button) (subscribe to device connector of push button)
# if Harr says that there is a face notify the owner of an existance of a face.


"""{
              "type": "REST_API",
              "title": "image_capture",
              "description": "image capture",
              "meta": {},
              "apis": [
                {
                  "id": "4",
                  "title": "im_cap",
                  "description": "string",
                  "protocol": "string",
                  "url": "localhost:8088",
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



###  getting data
# look for services in SC
import json
import requests
import service_search
# with open('config_control.json','r') as file:
#     dict = json.load(file)
#     file.close()

url = service_search.search('http://localhost:8082','mqtt-broker-at-localhost')