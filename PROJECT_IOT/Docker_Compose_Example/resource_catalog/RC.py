import cherrypy
import time
import json
import requests
from threading import *

class Resource_cat:
    exposed = True

    def GET(self, *uri, **params):
        with open('logfile.json', 'r') as logfile:
            json_file = json.load(logfile)
        logfile.close()
        # print(json_file)
        return json.dumps(json_file)
    # maybe implement a filter using URI (future work)

    def POST(self):
        # get the json to be added from POST request body
        to_add= cherrypy.request.body.read()
        data=to_add.decode('utf-8')
        dict = json.loads(data)
        # print(dict)
        dict['Updated'] = (time.time())
        # print(dict)


        with open('logfile.json', 'r') as logfile:
            json_file = json.load(logfile)
        logfile.close()
        json_file["list_of_RCs"].append(dict)
        # print(json_file)
        resources_list = json_file["list_of_RCs"]
        with open('logfile.json', 'w') as logfile:
            json.dump(json_file, logfile)
        logfile.close()

        return json.dumps(json_file)


    def PUT(self):
        #get data from PUT request body
        to_edit = cherrypy.request.body.read()
        data = to_edit.decode('utf-8')
        dict = json.loads(data)

        # get data from registered resources
        with open('logfile.json', 'r') as logfile:
            json_file = json.load(logfile)
        logfile.close()


        # get the list of resources from the json-formatted log file
        resources_list= json_file["list_of_RCs"]


        for R in resources_list:
            if dict['name']==R['name']:
                # print('\n\n found it\n \n')
                RC_list_index =resources_list.index(R)

                R = dict
                R['Updated'] = ((time.time()))
                # print('ok01')
                # print(RC_list_index)
                # print(type((RC_list_index)))
                resources_list[RC_list_index]=dict
                # print('ok02')


        print(resources_list)
        json_file['list_of_RCs'] = resources_list
        # print(json_file)

        # backing things up
        with open('logfile.json', 'w') as logfile:
            json.dump(json_file, logfile)
        logfile.close()
        return json.dumps(json_file)

    def DELETE(self,*uri):
        #get data from DEL request body
        print('1')
        with open('logfile.json', 'r') as logfile:
            json_file = json.load(logfile)
        logfile.close()
        resources_list = json_file["list_of_RCs"]
        for R in resources_list:
            #removing only the first name that match
            if R['name'] == uri[0]:
                # print(resources_list)
                resources_list.remove(R)
                # print(resources_list)
        # backing things up
        with open('logfile.json', 'w') as logfile:
            json.dump(json_file, logfile)
        logfile.close()
        return str(resources_list)


class  sc_registration_thread(Thread):
    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
        url ="http://localhost:8087"
        url ="http://localhost:8082/"

    def run(self):
        # registering and updating of the registration
        myobj = """{
                          "type": "REST_API",
                          "title": "Resource_CATALOG",
                          "description": "RC",
                          "meta": {},
                          "apis": [
                            {
                              "id": "3",
                              "title": "RC",
                              "description": "none", 
                              "protocol": "REST",
                              "url": "http://localhost:8087",
                              "spec": {
                                "mediaType": "JSON",
                                "url": "http://RC:8087",
                                "schema": {}
                              },
                              "meta": {}
                            }
                          ],
                          "doc": "http://RC:8097",
                          "ttl": 3
                        }"""

        url = 'http://linksmart:8082/'  # when using a docker container
        # url = 'http://localhost:8082/' #
        while True:
            try:
                x = requests.post(url, myobj)
                ID = json.loads(x.text)['id']
                print(f'id is {ID}')
                print('registration succeeded\nID is {}'.format(ID))
                while True:
                    try:
                        x = requests.put(url + ID, myobj)
                        ID = json.loads(x.text)['id']
                        print('update succeeded\nID is {}'.format(ID))
                        time.sleep(5)
                    except:
                        print('update failed with the host')
            except:
                print('registration failed with the host')
                time.sleep(5)



class delete_thread(Thread):
    def __init__(self, thread_ID):
        Thread.__init__(self)
        self.thread_ID = thread_ID
    def run(self):
        while True:
            x= requests.get("http://localhost:8087").json()
            if x['list_of_RCs'] == []:
                pass
            else:
                resources_list = x['list_of_RCs']
                print(resources_list)
                for R in resources_list:
                    if time.time() - (R['Updated']) > 5:
                        print(f'deleting one service\n{R["name"]}')
                        requests.delete('http://localhost:8087'+'/'+R['name'])
                        print('deleted successfully')
            time.sleep(2)









if __name__ == '__main__':
    # Res = {"outer_part": "hello",
    #        "list_of_RCs": [{ "name": "motion","ID": 1,"protocol": "REST","URL":"url", "Updated": time.ctime(time.time())}]}
    #
    # with open('logfile.json', 'w') as logfile:
    #     json.dump(Res, logfile)
    # logfile.close()

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
