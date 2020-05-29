FROM python:3
ADD get_data.py /
COPY get_data.py /get_data.py
RUN pip install pipreqs
RUN mkdir pipreqs_folder
RUN cp get_data.py pipreqs_folder/get_data.py
RUN pipreqs pipreqs_folder
RUN pip install -r pipreqs_folder/requirements.txt
CMD ["python", "./get_data.py"]