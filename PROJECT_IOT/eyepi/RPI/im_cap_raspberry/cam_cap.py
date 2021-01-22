import time
import picamera
import numpy as np
import cv2
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 24
    time.sleep(0.2)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    print(output)
    print(type(output))
    print(gray.shape)