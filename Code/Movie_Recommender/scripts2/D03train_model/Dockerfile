FROM python:3.7
RUN pip install numpy
RUN pip install scikit-surprise
ENV pystep=train_model.py
ADD $pystep /
COPY $pystep /$pystep
RUN pip install pipreqs
RUN mkdir pipreqs_folder
RUN cp $pystep pipreqs_folder/$pystep
RUN pipreqs pipreqs_folder
RUN pip install joblib
RUN pip install -r pipreqs_folder/requirements.txt
