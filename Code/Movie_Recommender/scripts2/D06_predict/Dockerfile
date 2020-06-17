FROM python:3.7-slim
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip3 install Flask gunicorn
CMD ["python", "app.py", "--port", $PORT]





