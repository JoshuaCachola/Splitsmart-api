# pull python image for container
FROM python:3.10.1-slim-buster

# set directory for application
WORKDIR /usr/src/app

# set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

# copy and install dependencies
COPY ./requirements.txt .
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# copy app to pwd
COPY . .

# copy entrypoint.sh
COPY ./entrypoint.sh .

# add execuatable to entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

