import numpy as np
a = np.array([1,2,3,4,5,6,8,9])
b = np.reshape(a,(-1,4))
print(a)
print(b)
print(b.shape[0])
c = np.squeeze(np.reshape(b,(1,8)))
print(c)