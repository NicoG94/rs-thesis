FROM python:3
ADD get_data.py /
COPY get_data.py /get_data.py
RUN pip install pandas
CMD ["python", "./get_data.py"]