import requests

def search(sc_url='http://localhost:8082',service_title=None):
    response_dict = requests.get(sc_url).json()
    service_list = response_dict['services']
    if service_title == None:
        return service_list
    else:
        state = False
        url = ' '
        # print(len(service_list))
        for S in service_list:
            # print(S['title'])
            # print(service_title)
            if service_title == S['title']:
                url = S['apis'][0]['url']
                state = True
        # print('the output is {} {}'.format(state,url))
        return state,url


