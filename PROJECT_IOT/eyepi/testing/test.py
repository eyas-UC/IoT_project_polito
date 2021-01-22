# import cherrypy
import time
import json
import requests
# from threading import *
# import registration as reg
import threading
global open_state
import lib

class  cherry_thread(threading.Thread):

    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        while 1:
            time.sleep(1)
            # print()
            print(lib.miorio(time.ctime(time.time())))

if __name__ == '__main__':
    a3 = cherry_thread(3)
    a3.start()
    a3.join()