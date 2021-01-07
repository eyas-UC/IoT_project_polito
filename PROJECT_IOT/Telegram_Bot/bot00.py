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
        # Local token
        self.tokenBot = token
        # Catalog token
        # self.tokenBot=requests.get("http://catalogIP/telegram_token").json()["telegramToken"]
        try:
            print('setting up bot')
            self.bot = telepot.Bot(self.tokenBot)
            self.bot.deleteWebhook()
            print('set up complete')
            self.chatIDs=[]
        except:
            print('settup failed    ')
        self.__message={"alert":"","action":""}
        MessageLoop(self.bot, {'chat': self.on_chat_message}).run_as_thread()

    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        self.chatIDs.append(chat_ID)
        message = msg['text']
        if message == "/switchOn":
            payload = self.__message.copy()
            payload['e'][0]['v'] = "on"
            payload['e'][0]['t'] = time.time()
            self.client.myPublish(self.topic, payload)
            self.bot.sendMessage(chat_ID, text="Led switched on")
        elif message == "/switchOff":
            payload = self.__message.copy()
            payload['e'][0]['v'] = "off"
            payload['e'][0]['t'] = time.time()
            self.client.myPublish(self.topic, payload)
            self.bot.sendMessage(chat_ID, text="Led switched off")
        elif message=="/start":
            self.bot.sendMessage(chat_ID, text="Welcome")
        else:
            self.bot.sendMessage(chat_ID, text="Command not supported")

    def POST(self,*uri):
        tosend=''
        output={"status":"not-sent","message":tosend}
        if len(uri)!=0:
            if uri[0]=='temp':
                body=cherrypy.request.body.read()
                jsonBody=json.loads(body)
                alert=jsonBody["alert"]
                action=jsonBody["action"]
                tosend=f"ATTENTION!!!\n{alert}, you should {action}"
                output={"status":"sent","message":tosend}
                for chat_ID in self.chatIDs:
                    print(chat_ID)
                    self.bot.sendMessage(chat_ID, text=tosend)
        return json.dumps(output)



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

class  sc_registration_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        # registering and updating of the registration
        # url = 'http://linksmart:8082/'  # when using a docker container
        url = 'http://localhost:8082/'
        reg.registration('bot_REST.json', url,'bot')


if __name__ == "__main__":
    a2 = sc_registration_thread(2)
    a3 = cherry_thread(3)
    a2.start()
    a3.start()
    a2.join()
    a3.join()
