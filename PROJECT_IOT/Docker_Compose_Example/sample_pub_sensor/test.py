dict = {"outer_part": "hello", "list_of_RCs": [ {"resource_name": "motion01", "type": "MQTT", "topic": "home/motion01", "sensor_ID": "mot_sen_01", "description": "discription here", "meta": {}, "URL": "test.mosquitto.org", "port": 1883, "pin_number": 7, "Updated": 1601640224.1891172},{"resource_name": "led01", "type": "MQTT", "topic": "home/led01", "sensor_ID": "led_01", "description": "discription here", "meta": {}, "URL": "192.168.1.178", "port": 1883, "pin_number": 8, "Updated": 1601640221.8578188}]}

lista = dict['list_of_RCs']

print(lista['resource_name'])
 # if 'motion01' in lista:


