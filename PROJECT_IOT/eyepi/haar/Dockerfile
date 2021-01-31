FROM python
COPY . /app
WORKDIR /app
RUN dpkg --print-architecture
#RUN apt-get update
RUN apt-get -y install libglib2.0-0
RUN pip install opencv-python-headless
#RUN pip3 install numpy
RUN pip3 install cherrypy
RUN pip3 install requests


CMD ["python3","./haarREST.py"]