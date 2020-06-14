import pandas as pd
import argparse
from pathlib import Path


def prepare_data(df, nMostRated = None, nTopUser = None):
    # take only top 1000 most rated movies

    mostRatedMovieIds = df.groupby("imdbId").count().sort_values("userId", ascending=False).head(nMostRated).index

    dfMostRated = df[df["imdbId"].isin(mostRatedMovieIds)]

    if nTopUser is None:
        mostRatedUserIds = df.groupby("userId").count().sort_values("rating", ascending=False).index
    else:
        mostRatedUserIds = df.groupby("userId").count().sort_values("rating", ascending=False)[10:nTopUser + 10].index

    dfMostRated2 = dfMostRated[dfMostRated["userId"].isin(mostRatedUserIds)]

    dfPivot = dfMostRated2.pivot(index="userId", columns="imdbId", values="rating")
    return dfPivot

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
    df = prepare_data(df, nMostRated=100, nTopUser=100)

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)

    # save data
    df.to_csv(args.output_path)
    #df.to_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\prepared_data.csv")
