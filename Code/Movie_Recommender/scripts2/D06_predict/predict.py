import pandas as pd
from surprise import dump
from scipy import spatial
from time import time

def predict_new_user(newUser, path_to_preds, n_similar_users=20):
    start=time()
    preds_known_user = pd.read_csv(path_to_preds)
    dfPivot = preds_known_user.pivot(index="uid", columns="iids", values="rating")

    # append new user to data
    dfPivot = dfPivot.append(pd.DataFrame(newUser, index=['-99']))
    dfPivot = dfPivot.fillna(dfPivot.mean(axis=0))  # dfPivot.mean(axis=0))
    end=time()
    print("Reading preds and getting pivoted data took {} seconds".format(end-start))


    # calculate distance to each existing user
    # TODO: make quicker - numpy matrix ?! dask df?
    start=time()
    userDistance = {}
    for user in dfPivot.index:
        userDistance[user] = spatial.distance.euclidean(dfPivot.loc['-99'], dfPivot.loc[user])
    end=time()
    print("Calculating distances took {} seconds".format(end - start))

    start=time()
    # get top n similar users
    similarUsers = sorted(userDistance.items(), reverse=True, key=lambda x: -x[1])[:n_similar_users]
    similarUsersDict = {key[0]: 1/key[1] for key in similarUsers if key[0] != "-99"}

    # get top movies for similar users
    preds_simiar_user = preds_known_user[preds_known_user["uid"].isin(list(similarUsersDict.keys()))][["uid", "iids", "preds"]]

    reciprocal_sum = sum(similarUsersDict.values())
    similarUserWeight = {k: v / reciprocal_sum for k, v in similarUsersDict.items()}
    similarUserWeightDf = pd.DataFrame.from_dict(similarUserWeight, orient="index", columns=["weight"])

    # get weighted est rating per item
    preds_simiar_user_weight = preds_simiar_user.merge(similarUserWeightDf, left_on="uid", right_index=True, how="left")
    preds_simiar_user_weight["weight_pred"] = preds_simiar_user_weight["preds"]*preds_simiar_user_weight["weight"]
    weight_preds = preds_simiar_user_weight.groupby("iids").aggregate({"weight_pred":"sum"}).sort_values("weight_pred", ascending=False)

    r"""
    weight_item_preds = {}
    for item in preds_simiar_user["iids"].unique():
        est_rate_weight=0
        # get all preds for one item
        item_preds = preds_simiar_user[preds_simiar_user["iids"]==item]
        for user in item_preds["uid"].unique():
            weight=similarUserWeight[user]
            pred = item_preds[item_preds["uid"]==user].iloc[0]["preds"]
            est_rate_weight += weight*pred
        weight_item_preds[item]=est_rate_weight
    weight_item_preds = {k: v for k, v in sorted(weight_item_preds.items(),reverse=True, key=lambda item: item[1])}
    """

    # filter if newUser has already rated movie
    known_items = [int(x) for x in newUser.keys()]
    weight_preds = weight_preds.drop(known_items)

    end=time()
    print("Calculating the rest took {} seconds".format(end - start))
    return weight_preds.to_dict()["weight_pred"]

if __name__ == "__main__":
    newUser = {'114709': 3, '113189': 1, '114746': 5}
    path_to_preds = r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\predictions.csv"
    preds = predict_new_user(newUser, path_to_preds, n_similar_users=25)


    r"""
    # var1: read preds and pivot them 
    start=time()
    preds_known_user = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\predictions.csv")
    dfPivot = preds_known_user.pivot(index="uid", columns="iids", values="orig_ratings")
    end=time()
    print("Read preds & pivot took {} seconds".format(end - start))

    # var2: read pivot and get preds from sql 
    start=time()
    # TODO: make quicker - dask df?!
    # load pivoted data
    dfPivot2 = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\pivotedRatings.csv", index_col=0)
    end=time()
    print("Reading pivoted data took {} seconds".format(end-start))
    """