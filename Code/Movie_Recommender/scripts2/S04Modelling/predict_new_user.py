from scipy import spatial
import pandas as pd
from surprise import dump

def predict_new_user(newUser, pathToPivotData, pathToModel):
    # load pivoted data
    dfPivot = pd.read_csv(pathToPivotData, index_col=0)
    
    # append new user to data
    dfPivot = dfPivot.append(pd.DataFrame(newUser, index=['-99']))
    dfPivot = dfPivot.fillna(0)#dfPivot.mean(axis=0))
    
    # calculate distance to each existing user
    userDistance = {}
    for user in dfPivot.index:
        userDistance[user] = spatial.distance.euclidean(dfPivot.loc['-99'], dfPivot.loc[user])
    
    # get top n similar users
    n=20
    similarUsers = sorted(userDistance.items(), reverse=True,key=lambda x:-x[1])[1:n+1]
    similarUsersKeys = [key[0] for key in similarUsers]
    
    # load rs
    _, loaded_algo = dump.load(pathToModel)
    
    # get top movies for similar users
    preds = {}
    for user in similarUsersKeys:
        preds[user] = {}
        for movie in list(dfPivot):
            preds[user][movie] = loaded_algo.predict(uid = str(user), iid=str(movie))[3]
    predsDf = pd.DataFrame.from_dict(preds)
    
    # get top movies from average from top movies for similar users
    # TODO: add distance as weighting
    recommendedMovies = predsDf.mean(axis=1).sort_values(ascending=False)[:20].to_dict()
    print(recommendedMovies)
    return recommendedMovies

if __name__ == "__main__":
    pathToPivotData = r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Code\Movie_Recommender\data\pivotedRatings.csv"
    pathToModel = r"C:/Users/nicog/OneDrive/3. Semester - Masterthesis/Code/Movie_Recommender/models/simpleRS2"
    newUser = {"111161": 3, "109830": 1, "110912": 5}
    #recommendedMovies = predict_new_user(newUser, pathToPivotData, pathToModel)

    # weighted distance
    '''
    # get top n similar prods
    n = 20
    similarProds = sorted(prodDistance.items(), reverse=True, key=lambda x: -x[1])[1:n + 1]
    # weight == rel. reciprocal of distance
    similarProdsDict = {key[0]: 1/key[1] for key in similarProds}
    reciprocal_sum = sum(similarProdsDict.values())
    similarProdsWeight = {k: v/reciprocal_sum for k, v in similarProdsDict.items()}
    
    def weighted_mean(similarProdsWeight, labels):
        summedVals = 0
        for k, v in similarProdsWeight.items():
            summedVals += labels[k] * v
        return summedVals
    
    weighted_mean(similarProdsWeight, labels)

    '''