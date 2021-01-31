import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
import requests
import time
import cherrypy
import registration as reg
import threading
import paho.mqtt.client as mqtt
import service_search
import resource_search
import string2numpy as s2n
import cv2
from io import BytesIO
import numpy as np

# accepts list of dictionaries of resources
# returns the non-repeated list of house ids
def show_house_ID(lista):
    #given list of house names
    h_ID = []
    for element in lista:
        if element['house_ID'] not in h_ID:
            h_ID.append(element['house_ID'])
    return h_ID


class RESTBot:
    exposed = True

    def __init__(self, token,my_id = 'bot_mqtt'):
        # Local token
        self.tokenBot = token
        # Catalog token
        # self.tokenBot=requests.get("http://catalogIP/telegram_token").json()["telegramToken"]
        try:
            print('setting up bot')
            self.bot = telepot.Bot(self.tokenBot)
            self.bot.deleteWebhook()# needed for initialization otherwise an error will pop
            self.chatIDs = []
            # initialize an instance of an BOT MQTT client as well
            with open('initialization.json') as file:
                # print('opened file successfully')
                dicto = json.load(file)
                file.close()

            # check if the right service and resource catalogs are up
            #first SC

            self.service_catalog_url = dicto['sc_url']
            self.broker = dicto['broker']
            self.port = dicto['port']
            # print(dicto['sc_url_local'])
            try:
                self.sc_response = requests.get(dicto['sc_url'])
                print(self.sc_response)
            except:
                print('trying to connect to service catalog\nusing local address')
                try:
                    print(dicto['sc_url_local'])
                    self.sc_response = requests.get(dicto['sc_url_local'])
                except:
                    print('second try')
                    self.__init__(token)

            # print(self.broker,self.port)

            self.mqtt_instance = client(my_id , self.broker, self.port)
            print('bot mqtt instance created...')
            self.mqtt_instance.start()
            # self.mqtt_instance.isSubscriber = False
            self.mqtt_instance.mymessage = ''
            print('set up complete')
        except:
            print('settup failed...MQTT not available\nretrying... ')
            print(self.tokenBot)
            self.__init__(token)

        self.__message = {"alert": "", "action": ""}
        # MessageLoop(self.bot, {'chat': self.on_chat_message}).run_as_thread()
        MessageLoop(self.bot, {'chat': self.on_chat_message,'callback_query': self.on_callback_query}).run_as_thread()

    def display_all_resorces(self):
        # look for RC in SC then in RC find all RC according to house
        try:
            # print(self.__class__.__name__)
            state, RC_url = service_search.search(sc_url='http://localhost:8082', service_title='RC')
            # print(state, RC_url)
            # state ==> true means RC is found
            if state == True:
                self.active_resource_list = resource_search.r_search(sc_url=RC_url)
                print(self.active_resource_list)
                house_list = []
                for r in self.active_resource_list:
                    # create a list of available house IDs
                    if r["house_ID"] not in house_list:
                        house_list.append(r["house_ID"])
                print(f"house list is as follows {house_list}")
                dump_list = []
                dicto = {}
                # sort houses according this list of house ids
                for h in house_list:
                    for r in self.active_resource_list:
                        if h == r['house_ID']:
                            dump_list.append(r)
                            li = dump_list[:]
                            #li is a copy not referenced to dump_list which contain all single house resoureces
                    dicto[h] = li
                    dump_list.clear()

                # print(f"the second {dicto['02']}")
                self.resource_dict = dicto
                # the keys are house IDs
                # the values list of that house available resources
                return True
            #was able to update all resources
            else:
                return False
            # was not able to update resources

        except:
            print('SC not working properly')

    # register method must give name, house_no and chatI, users are stored in housecat.json
    def register(self,name="",house_no="",chatID=""):
        try: #read file
            with open("housecat.json") as file:
                content = json.load(file)
                lista = content['list']
                file.close()
        except:
            print('error reading housecat.json')


        try:
            dicto = {"house_no": house_no,"name": name,"chatID":chatID}
            lista.append(dicto)
            content['list'] = lista

            with open("housecat.json",'w') as file:
                json.dump(content,file,indent=4)
                file.close()
        except:
            print('error writing on housecat.json')

    def deregister(self,name="",house_no="",chatID=""):
        try: #read file
            with open("housecat.json") as file:
                content = json.load(file)
                lista = content['list']
                file.close()
        except:
            print('error reading housecat.json')
        print(f'the list is {lista}\n\n')

        try:
            #create a list of elements to be removed (in case of duplicates)
            to_be_removed=[]
            for user in lista:
                # add users with either name or chatID to the remove list
                if name ==user['name'] or chatID ==user['chatID']:
                    to_be_removed.append(user)
                    print(user)
            print((to_be_removed))
            try:
                for element in to_be_removed:
                    print(element)
                    lista.remove(element)
                    # print('element should be removed')
            except:
                print('all elements are removed')
            content['list'] = lista
            # print(content)

            with open("housecat.json",'w') as file:
                json.dump(content,file,indent=4)
                file.close()
        except:
            print('error writing on housecat.json')

    def authenticate(self):
        try:  # read file
            with open("housecat.json") as file:
                lista = json.load(file)['list']
                # print(lista)
                file.close()
        except:
            print('error in housecat.json')
        allowed = False
        for user in lista:
            if self.chatID == user['chatID']:
                allowed = True
                return allowed , user['house_no'],user['name']
        return allowed, "00",""


    # with open("housecat.json",'w') as file:

            # file.close()
# updates lists of dictionaries and the active houses id --> active_IDs
    def show_houses_dict(self):
        state, RC_url = service_search.search(sc_url='http://localhost:8082', service_title='RC')
        # print(state, RC_url)
        if state == True:
            resources_list = resource_search.r_search(sc_url='http://localhost:8087')
            self.houses_list_dict= []
            for rc in resources_list:
                if rc['house_ID'] not in self.houses_list_dict:
                    self.houses_list_dict.append(rc)
            self.active_IDs = show_house_ID(self.houses_list_dict)# remove duplicates and save id list
            # print(self.active_IDs)
            # print(self.houses_list_dict)


    # called when user choses one of the buttons after sending "/help" / "commands"
    def on_callback_query(self,msg):
        self.message = msg["data"]
        self.chatID = (msg['message']['chat']['id'])
        # print(f'callback message is {self.message}')
        # print(self.authenticate())
########################################################################
        # register
########################################################################
        if self.message =="register":
            state,self.house_no,self.name=self.authenticate()
            if state == True:
                self.bot.sendMessage(self.chatID, text=f'already registered')
            if state == False:
                self.bot.sendMessage(self.chatID, text=f'type "reg name XX"')

########################################################################
        # deregister
########################################################################
        elif self.message =="deregister":
            # check if already registered
            state,self.house_no,self.name = self.authenticate()
            if state == False:
                self.bot.sendMessage(self.chatID, text=f'already unregisterd')
            if state == True:
                self.bot.sendMessage(self.chatID, text=f'type "dereg name "')

########################################################################
        # lock
########################################################################
        elif self.message =="lock":
            state,self.house_no,self.name=self.authenticate()
            # servo01 is always the lock for the house
            # rc exist
            active =self.is_r_active(self.house_no+'servo01')
            print(active)
            print(state)
            if (active):
                # the resource is active
                if state == True:
                    self.mqtt_instance.mypub(f'home{self.house_no}/servo01', json.dumps({'e': {'v': "15"}}))
                    self.bot.sendMessage(self.chatID, text=f'onwer: {self.name}\nhouse no.{self.house_no}\nis locked now')
                else:
                    self.bot.sendMessage(self.chatID, text=f'not autherized to open house')
            else:
                self.bot.sendMessage(self.chatID, text=f'resource is NOT active')


########################################################################
#       unlock
########################################################################
        elif self.message =="unlock":
            state, self.house_no, self.name = self.authenticate()
            # servo01 is always the lock for the house
            # rc exist
            active = self.is_r_active(self.house_no + 'servo01')
            print(active)
            print(state)
            if (active==True):
                # the resource is active
                if state == True:
                    self.mqtt_instance.mypub(f'home{self.house_no}/servo01', json.dumps({'e': {'v': "105"}}))
                    self.bot.sendMessage(self.chatID, text=f'onwer: {self.name}\nhouse no.{self.house_no}\nis unlocked now')
            else:
                self.bot.sendMessage(self.chatID, text=f'resource is NOT active')

########################################################################
# LED control
########################################################################

        elif self.message =="switchLED":
            state, self.house_no, self.name = self.authenticate()
            if state == True:
                self.bot.sendMessage(self.chatID, text=f'switch on/off dev. no.')
            else:
                self.bot.sendMessage(self.chatID, text=f'resource is NOT active')


########################################################################
# taking picture
########################################################################

        elif self.message =="picture":
            try:
                state, self.house_no, self.name = self.authenticate()
                print(state)
                if state == True:
                    #Autherized
                    # now check if resource is active
                    # assuming a single camera 01
                    active = self.is_r_active(self.house_no + 'camera01')
                    print(active)

                    if active == True:
                        #device is active and user is autherized
                        # self.resource is now updated with all cam resources
                        # state, rc_url = service_search.search(sc_url='http://localhost:8082', service_title='RC')
                        # print(rc_url)
                        self.return_resource(self.house_no + 'camera01')
                        # self.resource is now updated
                        cam_url = "http://"+self.resource['URL']+':'+self.resource['port']
                        print(cam_url)
                        data = requests.get(cam_url).content  # retrieving data from im_cap.py [string]
                        my_array = s2n.string2numpy(data)
                        cv2.imwrite('buffer_file.jpg', my_array)
                        with open('buffer_file.jpg') as file:
                            # url = f'https://api.telegram.org/bot{self.tokenBot}/sendPhoto'
                            self.bot.sendPhoto(self.chatID, photo=open('buffer_file.jpg', 'rb'))
                            file.close()
                    else:
                        self.bot.sendMessage(self.chatID, text=f'cam not available')

                else:
                    self.bot.sendMessage(self.chatID, text=f'Not Autherized')
            except:
                print('issue in picture method')

########################################################################
# end of callback querry
########################################################################

    # this function should find if resource is active in the requested house
    def is_r_active(self,rc_name):
        self.display_all_resorces()
        exist = False
        for e in self.resource_dict[self.house_no]:
            if e['resource_name'] == rc_name:
                exist = True
        return  exist

    def return_resource(self,rc_name):
        for e in self.resource_dict[self.house_no]:
            if e['resource_name'] == rc_name:
                self.resource = e
                # self.resource["url"] referers to resource urls



        # called when user sends text message from telegram
    def on_chat_message(self, msg):

        self.show_houses_dict()
        content_type, chat_type, chat_ID = telepot.glance(msg)
        self.chatIDs.append(chat_ID)
        self.chatID =chat_ID

        message = msg['text'].lower()
        print(chat_ID)
        print(f'the message is {message}')
        ########################################################
        #                   display commands
        ########################################################
        if message == "help" or message== "commands":
            buttons1 = [[InlineKeyboardButton(text=f'LED ON/OFF', callback_data=f'switchLED'),
                InlineKeyboardButton(text=f'Lock', callback_data=f'lock'),
                InlineKeyboardButton(text=f'Unlock', callback_data=f'unlock')]]
            buttons2 = [[InlineKeyboardButton(text=f'picture', callback_data=f'picture'),
                InlineKeyboardButton(text=f'register', callback_data=f'register'),
                InlineKeyboardButton(text=f'deregister', callback_data=f'deregister'),]]
            keyboard1 = InlineKeyboardMarkup(inline_keyboard=buttons1)
            keyboard2 = InlineKeyboardMarkup(inline_keyboard=buttons2)

            self.bot.sendMessage(chat_ID, text='1st', reply_markup=keyboard1)
            self.bot.sendMessage(chat_ID, text='2st', reply_markup=keyboard2)
        # maybe try to seperate code for actual commands


        ########################################################
        #                  #register command                   #
        ########################################################
        elif  message[0:3] == "reg":
            new_name =message.split()[1]
            try:
                new_house_no =message.split()[2]
                ###############################################################
                # check if the it is already registered  before duplicating anything
                state, self.house_no,self.name = self.authenticate()
                print(new_name,self.name)
                if state == True :
                    ## chatID matches one of the users chat ID
                    self.bot.sendMessage(self.chatID, text=f'chat ID exist')
                    if new_name == self.name:
                        # same name
                        if new_house_no== self.house_no:
                            # same house number
                            self.bot.sendMessage(self.chatID, text=f'house no. matches(no need to register)')
                        else:
                            #different house no.
                            self.bot.sendMessage(self.chatID, text=f'each user must have only one house')


                elif state == False :
                    self.register(new_name, new_house_no, self.chatID)
                    self.bot.sendMessage(self.chatID, text=f'new user added')


                else:
                    self.bot.sendMessage(self.chatID, text=f'an error occured during registration')

            except:
                self.bot.sendMessage(self.chatID, text=f'use the correct format"')


        ########################################################
                          #deregister command
        ########################################################
        # for now i think you should just name to deregister users
        elif  message[0:5] == "dereg":
            name =message.split()[1]
            #house_no =message.split()[2]
            ###############################################################
            # check if the it is already unregistered
            state, self.house_no,self.name = self.authenticate()
            if state == False:
                self.bot.sendMessage(self.chatID, text=f'already unregisterd')
            if state == True:
                self.deregister(name)
        ########################################################
                          #display resources
        ########################################################
        # for now i think you should just name to deregister users
        elif message =="disp res":
            state = self.display_all_resorces()# update the active resource list
            if state == True:
                # updated correctly
                # print(self.__class__.__name__)
                names = []
                dummy = []
                for house in list(self.resource_dict.keys()) :
                    # house is a list containing available houses
                    rc_of_one_house =self.resource_dict[house]
                    for element in rc_of_one_house:
                        dummy.append(element['resource_name'])
                    names = dummy[:]
                    dummy.clear()
                    # send necessary info to their prespective users only.
                    # authenticate
                    state,self.house_no,self.name=self.authenticate()
                    if self.house_no == house:
                    # only ones prespective house info should arrive to him
                        self.bot.sendMessage(self.chatID, text=f'house {house} recources are\n{names} ')
                        break

        ########################################################
        # LED section
        ########################################################
        # message format "switch on 01"
        elif message[0:6] == "switch":
            print(message[0:6] )
            try:
                operation = message.split()[1] # either (on off)
                resource_no = message.split()[2]
                state, self.house_no, self.name = self.authenticate()
                # servo01 is always the lock for the house
                # rc exist
                active = self.is_r_active(self.house_no + 'led'+resource_no)
                if (active):
                    # the resource is active
                    if state == True:
                        # user is autherized to perform action
                        if operation == 'on':
                            self.mqtt_instance.mypub(f'home{self.house_no}/led'+resource_no, json.dumps({'e': {'v': True}}))
                            self.bot.sendMessage(self.chatID,text=f'onwer: {self.name}\nhouse no.{self.house_no}\ndev no {resource_no}')
                        elif operation == 'off':
                            self.mqtt_instance.mypub(f'home{self.house_no}/led'+resource_no, json.dumps({'e': {'v': False}}))
                            self.bot.sendMessage(self.chatID,text=f'onwer: {self.name}\nhouse no.{self.house_no}\ndev no {resource_no}')
                    else:
                        self.bot.sendMessage(self.chatID, text=f'not autherized')
                else:
                    self.bot.sendMessage(self.chatID, text=f'resource is NOT active')
            except:
                self.bot.sendMessage(self.chatID,text=f'switch on/off dev no')



        ########################################################
        # Else
        ########################################################
        else:
            self.bot.sendMessage(self.chatID, text=f'not supported')

    # actuation
    ################################################################
    def update_user_list(self):
        with open("housecat.json") as file:
            self.user_list = json.load(file)['list']
            # print(lista)
            file.close()

########################################################################
#   POST REQUEST handler
########################################################################

    def POST(self, *uri):
        try:
            tosend = ''
            print(f'post uri is {uri}')
            output = {"status": "not-sent", "message": tosend}
            if len(uri) != 0:

########################################################################
#               motion handler from controller
########################################################################

                if uri[0] == 'motion':
                    body = cherrypy.request.body.read()
                    jsonBody = json.loads(body)
                    print(jsonBody)
                    if jsonBody['e']['v'] == True:
                        # send info of each house only to its user
                        # state, self.house_no, self.name = self.authenticate()
                        try:  # read file
                            # update_user_list reads the housecat.json whuih contains
                            # users name house and chatID
                            self.update_user_list()
                            for element in self.user_list:
                                if element["house_no"] == jsonBody['bn']:
                                    self.bot.sendMessage(element["chatID"], text=f'motion in house no. {jsonBody["bn"]} sensor no {jsonBody["e"]["no"]}')
                        except:
                            print('error in housecat.json')
########################################################################
                # push button handler from controller
########################################################################
                if uri[0] == 'push_button':
                    body = cherrypy.request.body.read()
                    jsonBody = json.loads(body)
                    print(jsonBody)
                    if jsonBody['e']['v'] == True:
                        # update_user_list reads the housecat.json which contains
                        # users name house and chatID
                        self.update_user_list()
                        for element in self.user_list:
                            if element["house_no"] == jsonBody['bn']:
                                self.bot.sendMessage(element["chatID"], text=f'door bell is pressed in house no. {jsonBody["bn"]}  no {jsonBody["e"]["no"]}')
########################################################################
                # haar handler from controller
########################################################################
                if uri[0] == 'haar':
                    body = cherrypy.request.body.read()
                    jsonBody = json.loads(body)
                    print(jsonBody)
                    self.update_user_list()
                    # same thing send message to its respective house owner
                    for element in self.user_list:
                        if element["house_no"] == jsonBody['bn']:
                            self.house_no = jsonBody['bn']
                            self.name = element['name']
                            self.chatID = element['chatID']
                            # the person is autherized!! send him only
                            # isFace =jsonBody['e']['v']['Face']
                            no_faces = jsonBody['e']['v']['Number of detected faces']
                            self.bot.sendMessage(element['chatID'], text=f'detected {no_faces} face(s) at your door')
                            print(no_faces)
                    #################
                    #################
                    # capture image
                    #################
                    #################
                    print(f'the house no is {self.house_no}')
                    active = self.is_r_active(self.house_no + 'camera01')
                    print(active)
                    if active == True:
                        # device is active
                        # self.resource is now updated with all cam resources
                        # state, rc_url = service_search.search(sc_url='http://localhost:8082', service_title='RC')
                        # print(rc_url)
                        self.return_resource(self.house_no + 'camera01')
                        # self.resource is now updated
                        cam_url = "http://" + self.resource['URL'] + ':' + self.resource['port']
                        print(cam_url)
                        data = requests.get(cam_url).content  # retrieving data from im_cap.py [string]
                        my_array = s2n.string2numpy(data)
                        cv2.imwrite('buffer_file.jpg', my_array)
                        with open('buffer_file.jpg') as file:
                            # url = f'https://api.telegram.org/bot{self.tokenBot}/sendPhoto'
                            self.bot.sendPhoto(self.chatID, photo=open('buffer_file.jpg', 'rb'))
                            file.close()
                    else:
                        self.bot.sendMessage(self.chatID, text=f'camera not connected')

            # return json.dumps(output)
        except:
            print('problem with post')

    ################################################################

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
        ## write functions that checks conditions
        ## then calls smaller functions that performs the actual MQTT Actions
        ## function should get the name of resource and its number
        ## looking function ---> for all mqtt resources(mqtt 2sub2) and their numbers
        ## get data(done by being in on message function) and do action
        ## the recieved sensor data(json) should contain which house / user / client

        received_dict = json.loads(msg.payload.decode('utf-8'))
        print(received_dict)

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
        # print('msg is published')

    def stop(self):

        if (self.isSubscriber):
            self.mqtt_client.unsubscribe(self.topic)

        self.mqtt_client.loop_stop()
        print('loop stopped')
        self.mqtt_client.disconnect()
        print('disconnect gracefully')


class cherry_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID

    def run(self):
        conf = json.load(open("settings.json"))
        token = conf["telegram_token"]
        conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
        bot = RESTBot(token)
        cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8099})
        cherrypy.tree.mount(bot, '/', conf)
        cherrypy.engine.start()
        while 1:
            time.sleep(1)


class sc_registration_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
        with open('initialization.json') as file:
            self.dicto = json.load(file)
        # print(dict)
        file.close()

    def run(self):
        # registering and updating of the registration
        # url = 'http://localhost:8082/'  # when using a docker container
        # url = 'http://localhost:8082/'
        try:
            url = self.dicto['sc_url']
            reg.registration('bot_REST.json', url, 'bot')
        except:
            print('error in registration trying again')


if __name__ == "__main__":
    a2 = sc_registration_thread(2)
    a3 = cherry_thread(3)
    a2.start()
    a3.start()
    a2.join()
    a3.join()


