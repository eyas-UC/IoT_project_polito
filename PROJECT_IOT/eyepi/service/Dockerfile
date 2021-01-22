FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install cherrypy
RUN pip install requests
CMD python ./ser.py