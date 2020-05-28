FROM python:3.7
COPY requirements.txt /requirements.txt
RUN pip install numpy
RUN pip install -r requirements.txt
CMD ["/usr/bin/pip", "freeze"]