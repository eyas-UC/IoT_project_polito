FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install cherrypy
RUN pip install requests
EXPOSE 8080
EXPOSE 8081
EXPOSE 8082
EXPOSE 80
CMD python entry_point.py
CMD python ./index.py