print("Lets start V0.2.1") 
import pandas as pd
import argparse
from pathlib import Path
from surprise import SVD, Dataset, Reader
from surprise.model_selection.split import train_test_split
from surprise.model_selection import cross_validate
from surprise import accuracy
#from sklearn.externals.joblib import dump
from joblib import dump
import os

def train_model(df, make_cv=True, make_train_test_split=False, user_col="userId", item_col="imdbId", rating_col="rating"):
    reader = Reader(rating_scale=(1, 5))
    # df (Dataframe) – The d ataframe containing the ratings. It must have three columns, corresponding to the user (raw) ids, the item (raw) ids, and the ratings, in this order.
    df[user_col]=df[user_col].astype(str)
    df[item_col]=df[item_col].astype(str)
    data = Dataset.load_from_df(df[[user_col, item_col, rating_col]], reader)

    # data.raw_ratings[0]



    if make_train_test_split:
        trainset, testset = train_test_split(data, test_size=.25)
    else:
        trainset = data.build_full_trainset()

    algo = SVD()
    algo.fit(trainset)
    #trainset.to_raw_uid(1)

    if make_train_test_split:
        # predict ratings for the testset
        predictions = algo.test(testset)
        # Then compute RMSE
        accuracy.rmse(predictions)

    if make_cv:
        cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    # Compute predictions of the 'original' algorithm.
    predictions = algo.test(trainset.build_testset())

    # sample pred
    uid = str(1)  # raw user id (as in the ratings file). They are **strings**!
    iid = str(114709)  # raw item id (as in the ratings file). They are **strings**!
    a=algo.predict(uid, iid, verbose=True)

    print("Algo trained")
    return algo

def predict_dataset(df, model, user_col="userId", item_col="imdbId", rating_col="rating"):
    #reader = Reader(rating_scale=(1, 5))
    #data = Dataset.load_from_df(df[[user_col, item_col, rating_col]], reader)
    #trainset, testset = train_test_split(data, test_size=1.00)
    #predictions = model.test(testset)

    predictions_long=[model.predict(str(user), str(item),verbose=False) for user in df[user_col].unique() for item in df[item_col].unique()]

    # predictions to pandas df
    uids, iids, orig_ratings, preds, det=zip(*predictions_long)
    predictionsDf = pd.DataFrame()
    predictionsDf["uid"] = uids
    predictionsDf["iids"] = iids
    predictionsDf["preds"] = preds

    # merge orig ratings to preds
    predictionsDf2 = pd.merge(predictionsDf, df, left_on=["uid", "iids"], right_on=[user_col, item_col], how="left")

    return predictionsDf2[["uid", "iids", "preds", "rating"]]

if __name__ == "__main__":


    # get arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--output_path_model', type=str,
                        help='Path of the local file where the Output 1 data should be written.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--output_path_preds', type=str,
                        help='Path of the local file where the Output 1 data should be written.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--input_path', type=str,
                        help='Path of the local file containing the Input 1 data.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--make_cv', type=str,
                        help='If cross validation shall be applied')  # Paths should be passed in, not hardcoded
    parser.add_argument('--make_train_test_split', type=str,
                        help='If testset shall be created')  # Paths should be passed in, not hardcoded
    args = parser.parse_args()
    print(args)

    # read data
    # index="userId", columns="imdbId", values="rating"
    df = pd.read_csv(args.input_path)
    #df = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\prepared_data.csv")

    # train model
    print("start training")
    model = train_model(df, make_cv=args.make_cv, make_train_test_split=args.make_train_test_split)
    #model = train_model(df)

    # predict train data
    predictionsDf = predict_dataset(df, model)

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output_path_model).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_path_preds).parent.mkdir(parents=True, exist_ok=True)

    # save model
    #dump(model, r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data_folder\model.joblib", compress=3)
    dump(model, args.output_path_model, compress=3)
    print("model saved")

    file_mb = os.stat(args.output_path_model).st_size / 1000000
    print(f"Model has {file_mb} MB.")

    predictionsDf.to_csv(args.output_path_preds, index=False)
    #predictionsDf.to_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\predictions.csv", index=False)
    print("Predictions saved")
