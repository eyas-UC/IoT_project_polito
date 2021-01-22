import cherrypy
import requests
import threading
import time
import json

myobj = """{
			  "type": "simple_service",
			  "title": "SERV_1",
			  "description": "DD",
			  "meta": {},
			  "apis": [
			    {
			      "id": "2",
			      "title": "my_test_service",
			      "description": "string", 
			      "protocol": "string",
			      "url": "localhost:8080",
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
url = 'http://linksmart:8082/'
# url = 'http://localhost:8082/'


class HelloWorld(object):
    exposed = True

    def GET(self):
        r = requests.get('https://api.exchangeratesapi.io/latest').text
        return r


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.tree.mount(HelloWorld(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    while True:
        try:
            x = requests.post(url, myobj)
            ID = json.loads(x.text)['id']
            print(f'id is {ID}')
            print('registration succeeded\nID is {}'.format(ID))
            while True:
                try:
                    x = requests.put(url + ID, myobj)
                    ID = json.loads(x.text)['id']
                    print('update succeeded\nID is {}'.format(ID))
                    time.sleep(5)

                except:
                    print('update failed with the host')

        except:
            print('registration failed with the host')

cherrypy.engine.exit()


