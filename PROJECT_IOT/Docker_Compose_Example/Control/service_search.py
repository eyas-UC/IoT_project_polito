import requests

def search(sc_url,service_id):
    response_dict = requests.get(sc_url).json()
    service_list = response_dict['services']

    for S in service_list:
        if service_id == S['id']:
            url = S['apis'][0]['url']
            # print(f'the url is {url}')
            return url

