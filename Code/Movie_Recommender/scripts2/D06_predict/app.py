import os
from flask import Flask, request

from . import predict
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        print("GET print")
        return "GET"
    if request.method == 'POST':
        # get data from post request
        # TODO: correct post & get format with request
        data = {"test_key": "test_val"}

        # predict new user

        return data
    else:
        target = os.environ.get('TARGET', 'World')
        return 'Hello {}!\n'.format(target)

if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)