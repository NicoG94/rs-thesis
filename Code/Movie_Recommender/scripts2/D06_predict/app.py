import os
from flask import Flask, request
import argparse

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
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--port', type=str,
                        help='port')  # Paths should be passed in, not hardcoded
    args = parser.parse_args()
    print(args)

    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    from waitress import serve
    serve(app, host="0.0.0.0", port=args.port)
    # CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app | in Dockerfile