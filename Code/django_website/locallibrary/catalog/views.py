from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from surprise import dump
from scipy import spatial
import os
from google.cloud import storage

'''
import sys
pathToCode = r"C:/Users/nicog/OneDrive/3. Semester - Masterthesis/Code/Movie_Recommender/scripts"
sys.path.append(pathToCode)
from scripts.S04Modelling import predict_new_user
'''

gcp=False
#os.chdir("locallibrary")

def init_gs():
    pathToCredentials = "storage_credentials.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = pathToCredentials

def read_blob_gs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)
    return blob

def predict_new_user(newUser, pathToPivotData, pathToModel, n_similar_users = 20):
    # load pivoted data
    dfPivot = pd.read_csv(pathToPivotData, index_col=0)

    # append new user to data
    dfPivot = dfPivot.append(pd.DataFrame(newUser, index=['-99']))
    dfPivot = dfPivot.fillna(0)  # dfPivot.mean(axis=0))

    # calculate distance to each existing user
    # TODO: make quicker
    userDistance = {}
    for user in dfPivot.index:
        userDistance[user] = spatial.distance.euclidean(dfPivot.loc['-99'], dfPivot.loc[user])

    # get top n similar users
    n = n_similar_users
    similarUsers = sorted(userDistance.items(), reverse=True, key=lambda x: -x[1])[1:n + 1]
    similarUsersKeys = [key[0] for key in similarUsers]

    # load rs
    _, loaded_algo = dump.load(pathToModel)

    # get top movies for similar users
    preds = {}
    for user in similarUsersKeys:
        preds[user] = {}
        for movie in list(dfPivot):
            preds[user][movie] = loaded_algo.predict(uid=str(user), iid=str(movie))[3]
    predsDf = pd.DataFrame.from_dict(preds)

    # get top movies from average from top movies for similar users
    # TODO: add distance as weighting
    recommendedMovies = predsDf.mean(axis=1).sort_values(ascending=False)[:20].to_dict()
    print(recommendedMovies)
    return recommendedMovies

def index(request):
    return render(request, 'index.html')

def read_gs_as_bytes_to_df(bucket_name, file_name, index_col=None):
    blob = read_blob_gs(bucket_name, file_name)
    data = blob.download_as_string()
    from io import StringIO
    s = str(data, 'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data, index_col=index_col)
    return df

def rating(request):
    # read example data, hardcoded
    if gcp:
        init_gs()

        print("HIIIIIIIER")
        print(os.getcwd())
        print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

        bucket_name = "movie_data_2603"
        file_name = "website_data/images.csv"
        imagesDf = pd.read_csv('gs://{}/{}'.format(bucket_name, file_name))[:16]
        #print(imagesDf)
        #imagesDf = read_gs_as_bytes_to_df(bucket_name, file_name)

    else:
        imagesDf = pd.read_csv(r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Code\django_website\locallibrary\images.csv")[:16]

    imagesDf.index = imagesDf.index.map(str)
    imagesDf.tconst = imagesDf.tconst.astype(str)
    returnDict = {"imagesDict": imagesDf.to_dict(orient="index")}

    return render(request, 'rating.html', returnDict)

def recommends(request):
    ''' function to show website and predict '''
    if gcp:
        init_gs()
    # get user ratings
    allRatingsToReturn = {}
    allRatings = request.META['QUERY_STRING'].split("&")
    for rating in allRatings:
        allRatingsToReturn[rating.split("=")[0]] = rating.split("=")[1]
    returnDict = {"allRatingsToReturn": allRatingsToReturn}

    # get new ratings in correct format
    # newUser = {'114709': 3, '113189': 1, '114746': 5}
    newUser = {str(k.split("rating")[1]):int(v) for k, v in allRatingsToReturn.items()}


    # predict movies for user

    # recommendedMovies = {'111161': 4.409709068218141, '169547': 4.367181866449892, '468569': 4.354459999567657, '1375666': 4.328690624281592, '110912': 4.293088068918457, '73486': 4.284921929324779, '83658': 4.263682846128104, '137523': 4.251407378217174, '68646': 4.246141097451418, '211915': 4.243610261700572, '75314': 4.239882627616437, '110413': 4.207163161515406, '71853': 4.206800296604597, '119217': 4.19738925719694, '338013': 4.188895711550159, '108052': 4.180040213386975, '114814': 4.163534871252197, '78748': 4.131342352280687, '120815': 4.127784049119275, '102926': 4.12774532343936}
    if gcp:
        bucket_name = "movie_data_2603"
        file_name = "prepared_data/pivotedRatings.csv"
        model_file = "models/simpleRS2"
        pathToPivotData = 'gs://{}/{}'.format(bucket_name, file_name)
        pathToModel = 'gs://{}/{}'.format(bucket_name, model_file)
    else:
        pathToPivotData = r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Code\Movie_Recommender\data\pivotedRatings.csv"
        pathToModel = r"C:/Users/nicog/OneDrive/3. Semester - Masterthesis/Code/Movie_Recommender/models/simpleRS2"

    recommendedMovies = predict_new_user(newUser, pathToPivotData, pathToModel)

    # get return df
    recommendedMoviesDf = pd.DataFrame(recommendedMovies.values(), index=recommendedMovies.keys(), columns=["estRate"])
    # recalculate estRate to scale 0-100
    recommendedMoviesDf["estRate"] = round(recommendedMoviesDf["estRate"]/5*100,1)

    # append moviename & imagepath
    if gcp:
        bucket_name = "movie_data_2603"
        file_name = "website_data/images.csv"
        imagesDf = pd.read_csv('gs://{}/{}'.format(bucket_name, file_name), index_col=0)
    else:
        imagesDf = pd.read_csv(r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Code\django_website\locallibrary\images.csv", index_col="tconst")
    imagesDf.index = imagesDf.index.map(str)
    recommendedMoviesDfReturn = recommendedMoviesDf.merge(imagesDf, left_index=True, right_index=True).to_dict('index')
    returnDict["recommendedMoviesDfReturn"] = recommendedMoviesDfReturn

    return render(request, 'recommends.html', returnDict)




