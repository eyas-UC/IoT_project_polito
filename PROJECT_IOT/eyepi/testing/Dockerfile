FROM python:3.7.9-slim-buster
COPY . /app
WORKDIR /app
#RUN pip3 install cherrypy
RUN pip3 install requests
RUN pip3 install threaded
#RUN pip3 install times
CMD ["python3","./test.py"]

#docker run -it --name container_name image_name 
#-it input and terminal