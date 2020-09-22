import cherrypy
import time
import json
import requests

Res = {"outer_part": "hello", "list_of_RCs": [{"id": 623, "name": "push button", "Updated": time.ctime(time.time())}]}

with open('data.json', 'w') as logfile:
    json.dump(Res, logfile)
logfile.close()


class Resource_cat:
    exposed = True

    def GET(self, *uri, **params):
        with open('data.json', 'r') as logfile:
            json_file = json.load(logfile)
        logfile.close()
        print(json_file)
        return str(json_file["list_of_RCs"])

    def POST(self):
        to_add= cherrypy.request.body.read()
        data=to_add.decode('utf-8')

        dict = json.loads(data)
        print(dict)
        dict['Updated'] = time.ctime(time.time())
        print(dict)

        with open('data.json', 'r') as logfile:
            json_file = json.load(logfile)
        logfile.close()
        json_file["list_of_RCs"].append(dict)
        print(json_file)

        with open('data.json', 'w') as logfile:
            json.dump(json_file, logfile)
        logfile.close()

        return 'success'





if __name__ == '__main__':
    conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
    cherrypy.tree.mount(Resource_cat(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8087})
    cherrypy.engine.start()
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
                      "url": "http://RC:8097",
                      "spec": {
                        "mediaType": "JSON",
                        "url": "string",
                        "schema": {}
                      },
                      "meta": {}
                    }
                  ],
                  "doc": "http://RC:8097",
                  "ttl": 3
                }"""

    url = 'http://linksmart:8082/'

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

    cherrypy.engine.exit()
