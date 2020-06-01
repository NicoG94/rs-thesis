FROM python:3
ENV pystep=get_data.py
ADD $pystep /
COPY $pystep /$pystep
RUN pip install pipreqs
RUN mkdir pipreqs_folder
RUN cp $pystep pipreqs_folder/$pystep
RUN pipreqs pipreqs_folder
RUN pip install -r pipreqs_folder/requirements.txt
RUN pip install google-cloud-storage
RUN curl -u 6779b8fa99386a1d132d71b1675c6237af4cb50b:x-oauth-basic https://raw.githubusercontent.com/NicoG94/rs-thesis/master/Code/Movie_Recommender/storage_credentials.json > out.json
RUN export GOOGLE_APPLICATION_CREDENTIALS="/out.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="/out.json"
CMD ["python", "get_data.py"]