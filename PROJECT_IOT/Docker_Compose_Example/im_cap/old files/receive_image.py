import cherrypy
import cv2
import time
import requests
import json
import numpy as np



# url = 'http://localhost:8082/'
class HelloWorld(object):
    exposed = True

    def GET(self):
        
        print('receiving image')
        try:
          print('before request')

          content =requests.get('http://127.0.0.1:8090/')
          print('after request')
          image = content['image']
          print('ok so far')
          new = np.fromstring(image,dtype = int)
          return new
        except:
            print('something went wrong')
            return ('something went wrong receiving')


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.tree.mount(HelloWorld(), '/', conf)
    cherrypy.config.update({'server.socket_host': 'localhost'})
    cherrypy.config.update({'server.socket_port': 8070})
    cherrypy.engine.start()
    cherrypy.engine.block()
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


    