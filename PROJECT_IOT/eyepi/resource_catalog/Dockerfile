#FROM python:3.7-slim-stretch
FROM python:rc-buster
COPY . /app
WORKDIR /app
RUN pip3 install cherrypy
RUN pip3 install requests
RUN pip3 install threaded
#RUN pip3 install pipwin
#RUN pipwin install jsonlib
#RUN pip3 install times
EXPOSE 8087
CMD ["python3","./RC.py"]
