from threading import *
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module
from registration import *
GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)


class client():
    def __init__(self, clientID, broker, port):
        self.clientID = clientID
        self.broker = broker
        self.port = port
        print('broker={},port={}'.format(broker, port))
        # initializing an instance
        self.mqtt_client = mqtt.Client(clientID)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message_r
        self.mqtt_client.on_log = self.on_log

    def on_log(self, paho_mqtt, usertdata, level, buf):
        # print('log: '+buf)
        pass

    def on_connect(self, paho_mqtt, userdata, flags, rc):
        if rc == 0:
            print('connected to the broker {}'.format(self.broker))

        else:
            print(f'bad connection')

    def on_message_r(self, paho_mqtt, userdata, msg):
        print('you received: ' + msg.payload.decode('utf-8'))
        if msg.payload.decode('utf-8') == "ON":
            GPIO.output(8, GPIO.HIGH)  # Turn on
            # sleep(1)                  # Sleep for 1 second
        elif msg.payload.decode('utf-8') == "OFF":
            GPIO.output(8, GPIO.LOW)  # Turn off
            # sleep(1)                  # Sleep for 1 second

    def mySub(self, topic):
        print('subscribing to {}'.format(topic))
        self.mqtt_client.subscribe(topic)
        self.isSubscriber = True
        self.topic = topic

    def start(self):
        self.mqtt_client.connect(self.broker, self.port)
        self.mqtt_client.loop_start()
        print('loop is started')

    def mypub(self, topic, msg):
        # print(topic+' '+ msg)
        self.mqtt_client.publish(topic, msg, 2)
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
                registration('led_config.json', url,'led01')
            except:
                print('error in registration')




if __name__ == '__main__':
    broker = 'test.mosquitto.org'
    #broker = '192.168.1.153'
    broker_port = 1883
    sensor_id = 'id_2'
    sensor1 = client(sensor_id, broker, broker_port)
    sensor1.start()
    sensor1.mySub('home/led01')
    a = rc_registration_thread(1)
    a.start()
    a.join()
    