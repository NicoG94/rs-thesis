FROM python:3
RUN apk add --update \
curl \
which \
bash
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
RUN mkdir gcp_data
RUN gsutil cp -r gs://rs_predictions gcp_data

ENV pystep=predict.py
ADD $pystep /
COPY $pystep /$pystep
RUN pip install pipreqs
RUN mkdir pipreqs_folder
RUN cp $pystep pipreqs_folder/$pystep
RUN pipreqs pipreqs_folder
RUN pip install -r pipreqs_folder/requirements.txt


