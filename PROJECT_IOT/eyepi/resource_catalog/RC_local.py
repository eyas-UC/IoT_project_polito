import cherrypy
import time
import json
import requests
# from threading import *
import registration as reg
import threading
global open_state

class Resource:
    def __init__(self):
        global  open_state
        open_state = False
        self.show_resource()

    def add_resource(self,dict):
        self.show_resource()
        # self.json_file  is updated
        self.resources_list.append(dict)
        # print(self.resources_list)
        # threadlock.acquire()
        global open_state
        if not open_state:
            open_state = True
            with open('logfile.json', 'w') as logfile:
                json.dump(self.json_file, logfile)
            logfile.close()
            open_state = False
        # threadlock.release()

    def show_resource(self):
        global open_state
        try:
            if not open_state:
                open_state = True
                with open('logfile.json', 'r') as logfile:
                    self.json_file = json.load(logfile)
                logfile.close()
                open_state = False
            self.resources_list = self.json_file["list_of_RCs"]
        except:
            reset_str = {"outer_part": "hello", "list_of_RCs": [],"delete_duration":25}
            # print(type(reset_str))
            print('error in config file now resetting it...')
            # threadlock.acquire()
            open_state = True
            with open('logfile.json', 'w') as logfile:
                self.json_file = json.dump(reset_str, logfile)
            logfile.close()
            open_state = False
            # threadlock.release()


    def update_resource(self,dict):
        self.show_resource()
        global open_state
        # get the list of resources from the json-formatted log file
        for R in self.resources_list:
            if dict['resource_name']==R['resource_name']:
                # print('\n\n found it\n \n')
                RC_list_index =self.resources_list.index(R)
                R = dict
                R['Updated'] = ((time.time()))
                self.resources_list[RC_list_index]=dict
        # threadlock.acquire()
        if not open_state:
            open_state = True
            with open('logfile.json', 'w') as logfile:
                json.dump(self.json_file, logfile)
            logfile.close()
            open_state = False
        # threadlock.release()
    def delete_resource(self,name):
        # get data from DEL request body
        global open_state
        self.show_resource()
        for R in self.resources_list:
            # removing only the first name that match
            if R['resource_name'] == name:
                # print(resources_list)
                self.resources_list.remove(R)
                # print(resources_list)
        # backing things up
        # threadlock.acquire()

        if not open_state:
            open_state = True
            with open('logfile.json', 'w') as logfile:
                json.dump(self.json_file, logfile)
            logfile.close()
            open_state = False
            # threadlock.release()


class Resource_cat:
    exposed = True

    def __init__(self):
        self.CAT = Resource()

    def GET(self):
        # self.CAT.json_file  will be updated
        self.CAT.show_resource()
        # print(json_file)
        return json.dumps(self.CAT.json_file)
    # maybe implement a filter using URI (future work)

    def POST(self):
        # get the json to be added from POST request body
        to_add= cherrypy.request.body.read()
        data=to_add.decode('utf-8')
        dict = json.loads(data)
        #updating time
        dict['Updated'] = (time.time())
        #adding the new resource to the log file
        self.CAT.add_resource(dict)
        # returning the new updated resource catalog json file
        self.CAT.json_file = self.CAT.show_resource()
        return json.dumps(self.CAT.json_file)


    def PUT(self):
        #get data from PUT request body
        to_edit = cherrypy.request.body.read()
        data = to_edit.decode('utf-8')
        dict = json.loads(data)

        self.CAT.update_resource(dict)
        self.CATjson_file = self.CAT.show_resource()
        return json.dumps(self.CAT.json_file)

    def DELETE(self,*uri):
        #get data from DEL request body
        self.CAT.show_resource()
        name_to_be_removed = uri[0]
        self.CAT.delete_resource(name_to_be_removed)
        self.CAT.show_resource()
        return json.dumps(self.CAT.json_file)


class  sc_registration_thread(threading.Thread):

    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        # registering and updating of the registration
        # url = 'http://linksmart:8082/'  # when using a docker container
        url = 'http://localhost:8082/'
        reg.registration('Resource_CATALOG.json', url,'RC')


class delete_thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        #time.sleep(10)
        while True:
        	try:
	            print('delete_thread')
	            x= requests.get("http://localhost:8087").json()
	            # print(f'x is {x}')
	            time.sleep(5)
	            # print(x)
	            resources_list = x['list_of_RCs']
	            # print(resources_list)
	            if not resources_list:
	                # empty
	                pass
	            else:
	                # print(resources_list)
	                for R in resources_list:
	                    # print('\n \ntype check')
	                    # print(type (   time.time()  )   )
	                    # print( type(float(R['Updated'] ))  )
	                    if time.time() -(float(R['Updated'])) > float(x['delete_duration']):
	                        print(f'deleting one service\n{R["resource_name"]}')
	                        # threadlock.acquire()
	                        requests.delete('http://localhost:8087'+'/'+R['resource_name'])
	                        # threadlock.release()
	                        print('deleted successfully')
	            time.sleep(8)
	        except:
	         	print('error in del thread')

class  cherry_thread(threading.Thread):

    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
        cherrypy.tree.mount(Resource_cat(), '/', conf)
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.config.update({'server.socket_port': 8087})
        cherrypy.engine.start()

if __name__ == '__main__':

    open_state = False
    threadlock = threading.Lock()
    a1 = delete_thread(1)
    a2 = sc_registration_thread(2)
    a3 = cherry_thread(3)
    a1.start()
    a2.start()
    a3.start()
    a1.join()
    a2.join()
    a3.join()