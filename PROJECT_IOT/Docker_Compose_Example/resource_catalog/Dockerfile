FROM python:3.7-slim-stretch
COPY . /app
WORKDIR /app
RUN pip3 install cherrypy
RUN pip3 install requests
CMD python ./RC.py