import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
import argparse


LOCAL = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--input_path', type=str,
                        help='Path of the local file containing the predictions.')  # Paths should be passed in, not hardcoded
    args = parser.parse_args()
    print(args)

    if LOCAL:
        preds = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\predictions.csv")
    else:
        preds = pd.read_csv(args.input_path)

    # drop na rows
    preds = preds.dropna(subset=["rating"])

    rmse = sqrt(mean_squared_error(preds["rating"], preds["preds"]))
    print(f"RMSE: {rmse}")

