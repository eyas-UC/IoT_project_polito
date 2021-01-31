import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
import requests
import time
import cherrypy
import registration as reg
import threading

class RESTBot:
    exposed=True
    def __init__(self, token):
        pass


    def POST(self):

        return json.dumps(output)



class cherry_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8099})
        cherrypy.tree.mount(bot, '/', conf)
        cherrypy.engine.start()

class  sc_registration_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        # registering and updating of the registration
        # url = 'http://linksmart:8082/'  # when using a docker container
        url = 'http://localhost:8082/'
        reg.registration('Control_REST.json', url,'bot')


if __name__ == "__main__":
    a2 = sc_registration_thread(2)
    a3 = cherry_thread(3)
    a2.start()
    a3.start()
    a2.join()
    a3.join()
