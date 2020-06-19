from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from surprise import dump
from scipy import spatial
import os
from google.cloud import storage
import requests



def index(request):
    return render(request, 'index.html')

def rating(request):
    # read example data, hardcoded
    imagesDf = pd.read_csv(r"images.csv")[:16]

    imagesDf.index = imagesDf.index.map(str)
    imagesDf.tconst = imagesDf.tconst.astype(str)
    returnDict = {"imagesDict": imagesDf.to_dict(orient="index")}

    return render(request, 'rating.html', returnDict)

def send_pred_request(newUser, pred_url):
    r = requests.post(pred_url, json=newUser)
    print(r.status_code)
    pred_dict = r.json()
    pred_dict = {k: v for k, v in sorted(pred_dict.items(), reverse=True, key=lambda item: item[1])}
    return pred_dict

def recommends(request):
    ''' function to show website and predict '''
    # get user ratings
    allRatingsToReturn = {}
    allRatings = request.META['QUERY_STRING'].split("&")
    for rating in allRatings:
        allRatingsToReturn[rating.split("=")[0]] = rating.split("=")[1]
    returnDict = {"allRatingsToReturn": allRatingsToReturn}

    # get new ratings in correct format
    # newUser = {'114709': 3, '113189': 1, '114746': 5}
    newUser = {str(k.split("rating")[1]):int(v) for k, v in allRatingsToReturn.items()}

    # recommendedMovies = {'111161': 4.409709068218141, '169547': 4.367181866449892, '468569': 4.354459999567657, '1375666': 4.328690624281592, '110912': 4.293088068918457, '73486': 4.284921929324779, '83658': 4.263682846128104, '137523': 4.251407378217174, '68646': 4.246141097451418, '211915': 4.243610261700572, '75314': 4.239882627616437, '110413': 4.207163161515406, '71853': 4.206800296604597, '119217': 4.19738925719694, '338013': 4.188895711550159, '108052': 4.180040213386975, '114814': 4.163534871252197, '78748': 4.131342352280687, '120815': 4.127784049119275, '102926': 4.12774532343936}

    # predict movies for user
    pred_url= "http://DESKTOP-LIQNDVB:8080"
    recommendedMovies = send_pred_request(newUser, pred_url)

    # get return df
    recommendedMoviesDf = pd.DataFrame(recommendedMovies.values(), index=recommendedMovies.keys(), columns=["estRate"])
    # recalculate estRate to scale 0-100
    recommendedMoviesDf["estRate"] = round(recommendedMoviesDf["estRate"]/5*100,1)

    # append moviename & imagepath
    imagesDf = pd.read_csv(r"imagess.csv", index_col="tconst")
    imagesDf.index = imagesDf.index.map(str)
    recommendedMoviesDfReturn = recommendedMoviesDf.merge(imagesDf, left_index=True, right_index=True).to_dict('index')
    returnDict["recommendedMoviesDfReturn"] = recommendedMoviesDfReturn

    return render(request, 'recommends.html', returnDict)

