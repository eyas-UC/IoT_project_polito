FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install numpy
RUN pip3 install glob3
RUN pip install cv2
CMD python ./REST_learn.py