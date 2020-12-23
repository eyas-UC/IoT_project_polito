import glob
import cv2
import numpy as np
from tools import *
# files =r"C:\huawei\DNN\OwnCollection\vehicles\Far\*.png"
files = "D:/POLITO/IOT/online/PROJECT_IOT/DNN/01.jpg"
count = 0
for f in glob.glob(files):
    img = cv2.imread(f, 0)#black and white
    img = img[np.newaxis, :, :]

train_x = img / 255.



layers_dims = [1, 6,6, 5, 1]
parameters = L_layer_model(train_x, 1, layers_dims,learning_rate=0.01, num_iterations=1000, print_cost=True)


