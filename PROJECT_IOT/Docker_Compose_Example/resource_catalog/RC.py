import cherrypy
import time
import json
import requests
from threading import *
import registration  as reg

class Resource:
    def __init__(self):
        self.show_resource()

    def add_resource(self,dict):
        self.show_resource()
        # self.json_file  is updated
        self.resources_list.append(dict)
        print(self.resources_list)
        with open('logfile.json', 'w') as logfile:
            json.dump(self.json_file, logfile)
        logfile.close()

    def show_resource(self):
        try:
            with open('logfile.json', 'r') as logfile:
                self.json_file = json.load(logfile)
            logfile.close()
            self.resources_list = self.json_file["list_of_RCs"]
        except:
            reset_str = {"outer_part": "hello", "list_of_RCs": []}
            print(type(reset_str))
            print('error in config file now resetting it...')
            with open('logfile.json', 'w') as logfile:
                self.json_file = json.dump(reset_str,logfile)
                logfile.close()


    def update_resource(self,dict):
        self.show_resource()
        # get the list of resources from the json-formatted log file
        for R in self.resources_list:
            if dict['resource_name']==R['resource_name']:
                # print('\n\n found it\n \n')
                RC_list_index =self.resources_list.index(R)
                R = dict
                R['Updated'] = ((time.time()))
                self.resources_list[RC_list_index]=dict

        with open('logfile.json', 'w') as logfile:
            json.dump(self.json_file, logfile)
        logfile.close()
    def delete_resource(self,name):
        # get data from DEL request body
        self.show_resource()
        for R in self.resources_list:
            # removing only the first name that match
            if R['resource_name'] == name:
                # print(resources_list)
                self.resources_list.remove(R)
                # print(resources_list)
        # backing things up
        with open('logfile.json', 'w') as logfile:
            json.dump(self.json_file, logfile)
        logfile.close()



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


class  sc_registration_thread(Thread):
    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
        url ="http://localhost:8087"
        url ="http://localhost:8082/"

    def run(self):
        # registering and updating of the registration

        # url = 'http://linksmart:8082/'  # when using a docker container
        url = 'http://localhost:8082/'
        reg.registration('Resource_CATALOG.json', url)

class delete_thread(Thread):
    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        #time.sleep(10)
        while True:
            x= requests.get("http://localhost:8087").json()
            time.sleep(3)
            #print(x)
            #print(type(x))
            #x=json.loads(x)
            # print(x)
            # print(type(x))
            resources_list = x['list_of_RCs']
            # print(resources_list)
            if not resources_list:
                
                pass
            else:
                print(resources_list)
                for R in resources_list:
                    # print('\n \ntype check')
                    # print(type (   time.time()  )   )
                    # print( type(float(R['Updated'] ))  )
                    if time.time() -(float(R['Updated'])) > 8:
                        print(f'deleting one service\n{R["resource_name"]}')
                        requests.delete('http://localhost:8087'+'/'+R['resource_name'])
                        print('deleted successfully')
            time.sleep(8)









if __name__ == '__main__':
    # Res = {"outer_part": "hello",
    #        "list_of_RCs": [{ "name": "motion","ID": 1,"protocol": "REST","URL":"url", "Updated": time.ctime(time.time())}]}
    #
    # with open('logfile.json', 'w') as logfile:
    #     json.dump(Res, logfile)
    # logfile.close()
    #
    conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
    cherrypy.tree.mount(Resource_cat(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8087})
    cherrypy.engine.start()
    a1 = delete_thread(1)
    a2 = sc_registration_thread(2)
    a1.start()
    a2.start()
    a1.join()
    a2.join()
    #cherrypy.engine.exit()
    #
    # R = Resource()
    # print(R.show_resource() )
    # dict = ({"name": "camera", "ID": 1, "protocol": "REST", "URL": "url", "Updated": 1601077207.2971442})
    # R.add_resource(dict)
    # print(R.show_resource())
