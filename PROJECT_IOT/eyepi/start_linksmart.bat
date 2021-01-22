@ECHO off
TITLE Setting UP
D:
CD D:\POLITO\IOT\PROJECT_IOT\Docker_Compose_Example\

ECHO ==== starting docker compose
REM %2
docker-compose build

ECHO ==== finished building 
REM %2
docker-compose up -d
REM %2
ECHO ==== Getting out of compose

cd service-catalog-master
docker run --name linksmart --network docker_compose_example_mynet -d -p 8082:8082 linksmart/sc
PAUSE
ECHO ====== test whateve lese
