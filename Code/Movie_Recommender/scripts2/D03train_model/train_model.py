import pandas as pd
import argparse
from pathlib import Path
from surprise import SVD, Dataset, Reader
from surprise.model_selection.split import train_test_split
from surprise.model_selection import cross_validate
from surprise import accuracy
from sklearn.externals.joblib import dump
import os

def train_model(df, make_cv=True, make_train_test_split=False, user_col="userId", item_col="imdbId", rating_col="rating"):
    reader = Reader(rating_scale=(1, 5))
    # df (Dataframe) – The d ataframe containing the ratings. It must have three columns, corresponding to the user (raw) ids, the item (raw) ids, and the ratings, in this order.
    data = Dataset.load_from_df(df[[user_col, item_col, rating_col]], reader)

    # data.raw_ratings[0]

    algo = SVD()

    if make_train_test_split:
        trainset, testset = train_test_split(data, test_size=.25)
    else:
        trainset = data.build_full_trainset()


    algo.fit(trainset)

    if make_train_test_split:
        # predict ratings for the testset
        predictions = algo.test(testset)
        # Then compute RMSE
        accuracy.rmse(predictions)

    if make_cv:
        cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    # Compute predictions of the 'original' algorithm.
    predictions = algo.test(trainset.build_testset())

    """
    # Dump algorithm and reload it.
    dump.dump(output_path, algo=algo)
    _, loaded_algo = dump.load(output_path)

    # We now ensure that the algo is still the same by checking the predictions.
    predictions_loaded_algo = loaded_algo.test(trainset.build_testset())
    assert predictions == predictions_loaded_algo
    print('Predictions are the same')
    """

    # sample pred
    uid = str(4094)  # raw user id (as in the ratings file). They are **strings**!
    iid = str(114709)  # raw item id (as in the ratings file). They are **strings**!
    pred = algo.predict(uid, iid, r_ui=4, verbose=True)
    print(pred)

    print("Algo trained")
    return algo

if __name__ == "__main__":
    print("Lets start V0.1.5")

    # get arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--output_path', type=str,
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
    df = pd.read_csv(args.input_path).head(1000)
    #df = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\merged_data.csv").head(1000)

    # train model
    print("start training")
    model = train_model(df, make_cv=args.make_cv, make_train_test_split=args.make_train_test_split)

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)

    # save model
    #path=r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data_folder\model.joblib"
    dump(model, args.output_path, compress=3)
    print("model saved")

    file_mb = os.stat(args.output_path).st_size / 1000000
    print(f"Model has {file_mb} MB.")