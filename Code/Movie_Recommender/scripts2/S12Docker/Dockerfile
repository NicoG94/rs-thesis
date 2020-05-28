FROM python:3.7
COPY requirements.txt /requirements.txt
RUN ["/usr/bin/pip", "install", "-r", "/requirements.txt"]
CMD ["/usr/bin/pip", "freeze"]