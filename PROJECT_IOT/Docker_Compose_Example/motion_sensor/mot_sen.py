import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import time
import json
import requests
from threading import *
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# get configuration file
with open('config.json', 'r') as settings_file:
    json_data = json.load(settings_file)
settings_file.close()



"""{
                  "resource_name": "motion_sensor",
                  "type": "MQTT",
                  "topic":"sens"
                  "sensor_ID":"mot_sen_01"
                  "description": "discription here",
                  "meta": {},
                  "URL": "192.168.1.178",
                  "port" :1883
                  "pin_number":7

                }"""

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
        url ="http://localhost:8087"
        url ="http://localhost:8087/"
        myobj ='{ "name": "test01","ID": 1,"protocol": "REST","URL":"url", "Updated": "temp"}'
    def run(self):
        while True:
            try:
                url ="http://localhost:8087/"
                myobj ='{ "name": "test01","ID": 1,"protocol": "REST","URL":"url", "Updated": "temp"}'
                print('ok')
                x = requests.post(url, myobj)
                print(x)
                print('ok1')
                #ID = json.loads(x.text)['id']
                #print(f'id is {ID}')
                print('registration succeeded\n')


                while True:
                    try:
                        x = requests.put(url, myobj)
                        #ID = json.loads(x.text)['id']
                        print('update succeeded\n')
                        time.sleep(2)

                    except:
                        print('update failed with the host')

            except:
                print('registration failed with the host')
                time.sleep(2)



class publish_thread(Thread):
    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        while True:
            i = GPIO.input(7)
            if i ==1:
                output = f'movement 1 and {time.ctime(time.time())}'
                sensor1.mypub(json_data['topic'],output)
                time.sleep(2)
            elif i == 0 :
                output = f'no movement 0 and {time.ctime(time.time())}'
                sensor1.mypub(json_data['topic'],output)
                time.sleep(2)



if __name__ == '__main__':
    sensor_id = json_data['sensor_ID']
    broker = json_data['URL']
    broker_port = json_data['port']
    sensor1 = client(sensor_id,broker,broker_port)
    sensor1.start()
    a1 = publish_thread(1)
    a2 = rc_registration_thread(2)
    a1.start()
    a2.start()
    a1.join()
    a2.join()
    
