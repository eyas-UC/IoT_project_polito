import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN) 



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


if __name__ == '__main__':
	broker = 'test.mosquitto.org'
	broker_port = 1883
	sensor_id = 'id_2'
	sensor1 = client(sensor_id,broker,broker_port)
	sensor1.start()
	GPIO.input(7)
	while True:
		if i ==1:
			output = f'value is 1 and {time.ctime(time.time())}'
			sensor1.mypub('sens',output)
		elif i == 0:
			output = f'value is 1 and {time.ctime(time.time())}'
			sensor1.mypub('sens',output)
		time.sleep(5)









