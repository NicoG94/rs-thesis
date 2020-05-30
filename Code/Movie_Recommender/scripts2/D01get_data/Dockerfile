FROM python:3
ENV pystep=get_data.py
ADD $pystep /
COPY $pystep /$pystep
RUN pip install pipreqs
RUN mkdir pipreqs_folder
RUN cp $pystep pipreqs_folder/$pystep
RUN pipreqs pipreqs_folder
RUN pip install -r pipreqs_folder/requirements.txt
CMD ["python", "get_data.py"]