# IoT_project_polito

##RESOURCE CATALOG
the goal of the Resource catalog is basically to list all the available resources represented by their corresponding Device Connector.
(from the slides of lecture 11)
The Resource Catalog is a device registry system. It registers
and provides a registry of available IoT devices and the
resources they expose. It exposes a simple JSON-based RESTful
API, which is intended to be used by:
• Device Connectors to register the available devices and their
resources
• Applications to discover these devices and learn how to talk
with them

our goal is creat a RESTfull API that can get all or certain resources using GET requests.
add new resources using POST
modify using PUT
deleting using Delete

the registered resource should be in this format(can be modified)

{"name":"Temp_01",
"ID":"0001",
"protocol": "MQTT/REST",
"URL":"url/broker URL",
"last_update":"time.time()"
}
