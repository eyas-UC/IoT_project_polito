# the received message will have the following structure.
        # {
        # "bn":"basename",
        # "e":{"n":"name", "no":"number","t":time","v","value"}
        # }
# for each house do the following
# base name --> homexx/sensors or homexx/actuator
# push button --> picture
# motion --> led + telegram
# face detected --> motor to unlock

import json

def number_handler(bn):
    word_list = bn.split('/')
    number = ''
    for char in word_list[0]:
        if char.isdigit():
            number += char
    if number == '':
        return 'wrong format'
    else:
        return int(number)


def dict_handler(self,dicto):
    basename = dicto['bn']
    house_no = number_handler(basename)
    sen_name = dicto['e']['n']
    sen_no = dicto['e']['no']
    time = dicto['e']['t']
    value = dicto['e']['v']
    # conditions here
    ##########################################
    if sen_name == 'motion':
        #pub message to led
        self.mypub('home/led01', json.dumps({'True'}))
        time.sleep(3)
        self.mypub('home/led01', json.dumps({'False'}))



#dict = { "bn":"home03/sensors","e":{"n":"motion","no":"01","t":"time","v":"value"}}

