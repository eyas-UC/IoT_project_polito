import requests

def search(sc_url='http://localhost:8082',service_id=None):
    response_dict = requests.get(sc_url).json()
    service_list = response_dict['services']
    if service_id == None:
        return service_list
    for S in service_list:
        if service_id == S['id']:
            url = S['apis'][0]['url']
            # print(f'the url is {url}')
            return url


