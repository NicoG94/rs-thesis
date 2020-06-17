#!/usr/bin/env python3
# Code/Movie_Recommender/scripts2/D06_predict/Dockerfile
# https://realpython.com/python-sockets/
"""

import socket

HOST = 'predict.dns.internal'  # Standard loopback interface address (localhost)
PORT = 80         # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            print("start")
            data = conn.recv(1024)
            if not data:
                print("NO DATA")
            #    break
            print(f"DATA: {data}")
            conn.sendall(data)
            print("END")

#df = pd.read_csv("gcp_data/rs_predictions/prepared_data.csv")
"""
import os
import shutil
import requests
import tempfile

from gevent.pywsgi import WSGIServer
from flask import Flask, after_this_request, render_template, request, send_file
from subprocess import call

app = Flask(__name__)

@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)


@app.route('/', methods=['GET', 'POST'])
def api():
    work_dir = tempfile.TemporaryDirectory()
    file_name = 'document'
    input_file_path = os.path.join(work_dir.name, file_name)
    # Libreoffice is creating files with the same name but .pdf extension
    output_file_path = os.path.join(work_dir.name, file_name + '.pdf')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file provided'
        file = request.files['file']
        if file.filename == '':
            return 'No file provided'
        if file and allowed_file(file.filename):
            file.save(input_file_path)

    if request.method == 'GET':
        url = request.args.get('url', type=str)
        if not url:
            return render_template('index.html')
        # Download from URL
        response = requests.get(url, stream=True)
        with open(input_file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response

    convert_file(work_dir.name, input_file_path)

    @after_this_request
    def cleanup(response):
        work_dir.cleanup()
        return response

    return send_file(output_file_path, mimetype='application/pdf')

if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    #from gevent.pywsgi import WSGIServer
    #http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    #http_server.serve_forever()

