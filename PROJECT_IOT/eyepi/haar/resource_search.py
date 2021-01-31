import requests

def r_search(sc_url='http://localhost:8087',resource_name=None):
    response_dict = requests.get(sc_url).json()
    service_list = response_dict['list_of_RCs']
    if resource_name == None:
        return service_list
    else:
        state = False
        url = ''
        port = ''
        topic = ''
    for S in service_list:
        if resource_name == S['resource_name']:
            url = S['URL']
            port = S['port']
            topic = S['topic']
            state = True
            # print(f't he url is {url}')
    return state,url, port, topic

# print(r_search(resource_name='led01'))

