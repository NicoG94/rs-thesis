import os
from flask import Flask, request
import argparse
import json

from predict import predict_new_user
#from scripts2.D06_predict.predict import predict_new_user
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        print("GET print")
        return "GET"
    if request.method == 'POST':
        # get data from post request
        data=json.loads(request.data)
        print(data)
        # TODO: correct post & get format with request
        #data = {'114709': 3, '113189': 1, '114746': 5}

        # predict new user
        preds = predict_new_user(newUser=data,
                         #path_to_preds="/mnt/predictions.csv", # live use
                         path_to_preds=r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\predictions.csv", # local use
                         n_similar_users=25)
        return preds
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

