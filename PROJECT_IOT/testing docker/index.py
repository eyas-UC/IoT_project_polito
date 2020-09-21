import cherrypy
import requests
import threading
import time
myobj = """{
			  "type": "rrrrrrrrr",
			  "title": "rrrrrr",
			  "description": "EEEEEEEEEEEEEe",
			  "meta": {},
			  "apis": [
			    {
			      "id": "2",
			      "title": "3",
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







class HelloWorld(object):
    exposed = True
    def GET(self):
        r = requests.get('https://api.exchangeratesapi.io/latest').text
        return r





if __name__ == '__main__':
	conf = {
	'/':{
		'request.dispatch':cherrypy.dispatch.MethodDispatcher()
	}
	}
	cherrypy.tree.mount (HelloWorld(),'/',conf)
	cherrypy.config.update({'server.socket_host': '0.0.0.0'})
	cherrypy.config.update({'server.socket_port': 8080})
	cherrypy.engine.start()
	while True:
			url = 'http://localhost:8082'
			url = 'http://www.google.com'
			# x = requests.post(url, data = myobj)
			x = requests.get(url)
			print(x)
			time.sleep(5)
			
	cherrypy.engine.exit()


	
