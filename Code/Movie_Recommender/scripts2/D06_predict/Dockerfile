FROM python:3.7-slim
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip3 install Flask gunicorn
RUN pip3 install waitress
CMD python3 app.py --port $PORT

