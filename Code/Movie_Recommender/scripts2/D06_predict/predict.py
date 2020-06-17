import pandas as pd
from surprise import dump
from scipy import spatial


def predict_new_user(newUser, pathToPivotData, pathToModel, n_similar_users=20):
    # TODO: make quicker - dask df?!
    # load pivoted data
    dfPivot = pd.read_csv(pathToPivotData, index_col=0)

    # append new user to data
    dfPivot = dfPivot.append(pd.DataFrame(newUser, index=['-99']))
    dfPivot = dfPivot.fillna(0)  # dfPivot.mean(axis=0))

    # calculate distance to each existing user
    # TODO: make quicker - numpy matrix ?! dask df?
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

if __name__ == "__main__":
    # df = pd.read_csv("gcp_data/rs_predictions/prepared_data.csv")
    train_data = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\prepared_data.csv")
    newUser = {'114709': 3, '113189': 1, '114746': 5}
    preds_known_user = 1