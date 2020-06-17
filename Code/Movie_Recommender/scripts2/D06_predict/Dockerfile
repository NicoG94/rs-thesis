FROM ubuntu:latest
RUN apt-get update
RUN apt-get install sudo
RUN sudo apt-get -y install \
python3 \
python3-pip \
curl \
bash

ENV APP_HOME /app
WORKDIR $APP_HOME
RUN pip3 install Flask gunicorn

RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
RUN mkdir gcp_data
RUN gsutil cp -r gs://rs_predictions gcp_data

ENV pystep=predict.py
ADD $pystep /
COPY $pystep /$pystep

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app





