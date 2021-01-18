FROM python:3.7-slim-stretch
COPY . /app
WORKDIR /app
RUN dpkg --print-architecture
# Install OpenCV's runtime dependencies
RUN apt-get update
RUN apt-get -y install libglib2.0-0
# Install OpenCV headless using pip
RUN pip install opencv-python-headless==4.1.0.25
RUN pip install numpy
RUN pip install requests
RUN pip install cherrypy
RUN python -c 'import cv2'
RUN python3 haarREST.py