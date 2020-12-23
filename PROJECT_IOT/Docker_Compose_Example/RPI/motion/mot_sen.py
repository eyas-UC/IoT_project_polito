import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import time
import json
import requests
from registration import *
from threading import *
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# get configuration file
with open('motion_config.json', 'r') as settings_file:
    json_data = json.load(settings_file)
settings_file.close()


GPIO.setup(json_data['pin_number'], GPIO.IN) 

class client():
    def __init__(self,clientID,broker,port):
        self.clientID = clientID
        self.broker = broker
        self.port = port
        print('broker={},port={}'.format(broker,port))
        # initializing an instance
        self.mqtt_client = mqtt.Client(clientID)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message_r
        self.mqtt_client.on_log = self.on_log

    def on_log(self,paho_mqtt,usertdata,level,buf):
        # print('log: '+buf)    
        pass

    def on_connect(self,paho_mqtt,userdata,flags,rc):
        if rc ==0:
            print('connected to the broker {}'.format(self.broker))

        else:
            print(f'bad connection')

    def on_message_r(self,paho_mqtt,userdata,msg):
        print('you received: '+msg.payload.decode('utf-8'))

    def mySub(self,topic):
        print('subscribing to {}'.format(topic))
        self.mqtt_client.subscribe(topic)
        self.isSubscriber = True
        self.topic =topic

    def start(self):
        self.mqtt_client.connect(self.broker,self.port)
        self.mqtt_client.loop_start()
        print('loop is started')

    def mypub(self,topic,msg):
        # print(topic+' '+ msg)
        self.mqtt_client.publish(topic,msg,2)
        print('msg is published')

    def stop(self):

        if (self.isSubscriber):
            self.mqtt_client.unsubscribe(self.topic)

        self.mqtt_client.loop_stop()
        print('loop stopped')
        self.mqtt_client.disconnect()
        print('disconnect gracefully')


class  rc_registration_thread(Thread):
    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        while True:
            try:
                url ="http://192.168.1.151:8087/"
                registration('motion_config.json', url,'motion01')
            except:
                print('error in registration')



class publish_thread(Thread):
    def __init__(self, thread_ID,pin,topic):
        Thread.__init__(self)
        self.thread_ID = thread_ID
        self.pin = pin
        self.topic = topic
    def run(self):
        while True:
            i = GPIO.input(self.pin)
            if i ==1:
                output = {'motion':True,'time':str(time.time())}
                sensor1.mypub(self.topic,json.dumps(output))
                
            elif i == 0 :
                pass
                #output = {'motion':False,'time':str(time.time())}
                #sensor1.mypub(self.topic,json.dumps(output))
            time.sleep(2)



if __name__ == '__main__':
    sensor_id = json_data['sensor_ID']
    broker = json_data['URL']
    broker_port = json_data['port']
    sensor1 = client(sensor_id,broker,broker_port)
    sensor1.start()
    a1 = publish_thread(1,json_data['pin_number'],json_data['topic'])
    a2 = rc_registration_thread(2)
    a1.start()
    a2.start()
    a1.join()
    a2.join()
    
