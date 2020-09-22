FROM python:3.7-slim-stretch
COPY . /app
WORKDIR /app
RUN pip install cherrypy
RUN pip install requests

CMD python ./RC.py