import cherrypy
import time
import json

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
