import pandas as pd
import argparse
from pathlib import Path


def prepare_data(df, min_ratings_user = 20, min_ratings_items = 20):
    # filter users & movies < 25 ratings and top 10 users
    user_upper_limit = sorted(df.groupby("userId").count()["rating"], reverse=True)[10]
    grouped_user = df.groupby("userId").count()["rating"]
    keep_user = grouped_user[(grouped_user > min_ratings_user) & (grouped_user < user_upper_limit)].index

    grouped_items = df.groupby("movieId").count()["rating"]
    keep_items = grouped_items[(grouped_items > min_ratings_items)].index

    dfPrepared = df[df["movieId"].isin(keep_items)]
    dfPrepared = dfPrepared[dfPrepared["userId"].isin(keep_user)]

    return dfPrepared


if __name__ == "__main__":
    print("Lets start V0.1.5")

    # get arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--output_path', type=str,
                        help='Path of the local file where the Output 1 data should be written.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--input_path', type=str,
                        help='Path of the local file containing the Input 1 data.')  # Paths should be passed in, not hardcoded
    args = parser.parse_args()
    print(args)

    # read data
    df = pd.read_csv(args.input_path)
    #df = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\merged_data.csv")

    # prepare data
    dfPrepared = prepare_data(df, min_ratings_user = 20, min_ratings_items = 25)

    # pivot data
    #dfPivot = dfPrepared.pivot(index="userId", columns="imdbId", values="rating")
    #dfPivot.to_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\pivotedRatings.csv")

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)

    # save data
    dfPrepared.to_csv(args.output_path)
    #dfPrepared.to_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\prepared_data.csv")
