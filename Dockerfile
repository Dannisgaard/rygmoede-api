FROM python:3.9

RUN mkdir /rygmoede
# set work directory
WORKDIR /rygmoede

# set environment variables
ENV PYTHONPATH=/rygmoede

EXPOSE 8080

# copy project
ADD . /rygmoede/
WORKDIR /rygmoede

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
