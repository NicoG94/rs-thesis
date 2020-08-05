FROM python:3.7
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN apt-get -y update
RUN apt-get -y upgrade
RUN pip3 install numpy
RUN pip3 install scikit-surprise
RUN pip3 install gcsfs
RUN apt-get -y install curl
RUN curl https://storage.googleapis.com/rs_predictions/predictions.csv --output /mnt/predictions.csv
RUN pip3 install Flask gunicorn
RUN pip3 install -r requirements.txt
CMD python3 app.py --port $PORT
