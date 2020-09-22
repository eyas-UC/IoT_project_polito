import numpy as np
a ='[1 2 3 4 5 6 8 9]'
a =a.replace('[','')
a=a.replace(']','')
# print(a)
my_array =np.fromstring(a,dtype=int,sep=' ')
print(my_array)
