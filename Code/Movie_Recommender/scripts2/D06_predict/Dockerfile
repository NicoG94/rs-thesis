FROM ubuntu:latest
RUN apt-get update
RUN apt-get install sudo
RUN sudo apt-get -y install \
python3 \
python3-pip \
curl \
bash
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
RUN mkdir gcp_data
RUN gsutil cp -r gs://rs_predictions gcp_data

ENV pystep=predict.py
ADD $pystep /
COPY $pystep /$pystep
RUN pip3 install pipreqs
RUN mkdir pipreqs_folder
RUN cp $pystep pipreqs_folder/$pystep
RUN pipreqs pipreqs_folder
RUN pip3 install -r pipreqs_folder/requirements.txt





