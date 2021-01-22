import paho.mqtt.client as mqtt
import time
from check import*
# import check

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


import time
from threading import *

class  a_thread(Thread):
	def __init__(self, thread_ID):
		Thread.__init__(self)
		self.thread_ID = thread_ID

	def run(self):
		for i in range(5):
			print(i)
			time.sleep(0.1)
			
			#print(time.ctime(time.time()))
		return time.ctime(time.time())



class mythread(a_thread):
	def run(self):
		print('changed')
		# mqtt_client.mypub('sens',self.clientID)


a1 = mythread(1)
a2 = mythread(2)

a1.start()
a2.start()
a1.join()
a2.join()





# if __name__ == '__main__':
# 	sensor1 = client('id_2','test.mosquitto.org',1883)
# 	sensor1.start()
# 	time1 = time.ctime(time.time())
# 	# print(time1)
# 	sensor1.mypub('sens',time1)
# 	# sensor1.publish('sens',time.ctime(time.time))


# 	# value = input('enter value')
# 	time.sleep(1)

# 	# client.loop_stop()
# 	# client.disconnect()








