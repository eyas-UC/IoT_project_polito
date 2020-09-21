FROM python:3
ADD haar.py / 
ADD haarcascade_frontalface_default.xml /
ADD requirements.txt /
RUN pip3 install -r requirements.txt
CMD ["python3","./haar.py"]