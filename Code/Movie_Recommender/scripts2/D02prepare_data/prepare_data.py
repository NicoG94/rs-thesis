import pandas as pd
import os
import logging
#from google.cloud import storage
import gcsfs
import argparse
from datetime import date
from pathlib import Path
from kfp.components import InputPath, OutputPath
from io import StringIO

def make_dir(temp_folder):
    # make folder and path
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

def get_pd_path(bucket_name, file_name):
    pathToLinks = 'gs://{}/{}'.format(bucket_name, file_name)
    return pathToLinks

def read_csv(path):
    #path = get_pd_path(bucket_name, file_name)
    df = pd.read_csv(path)
    return df

def str_to_df(str):
    return pd.read_csv(StringIO(str), sep=",")


def write_csv(df, bucket_name, file_name):
    path = get_pd_path(bucket_name, file_name)
    df.to_csv(path)
    print(f"{file_name} saved to bucket {bucket_name}")

def prepare_data(df, nMostRated = 100, nTopUser = 100):
    # take only top 1000 most rated movies

    mostRatedMovieIds = df.groupby("imdbId").count().sort_values("userId", ascending=False).head(nMostRated).index

    dfMostRated = df[df["imdbId"].isin(mostRatedMovieIds)]

    mostRatedUserIds = df.groupby("userId").count().sort_values("rating", ascending=False)[10:nTopUser + 10].index

    dfMostRated2 = dfMostRated[dfMostRated["userId"].isin(mostRatedUserIds)]

    dfPivot = dfMostRated2.pivot(index="userId", columns="imdbId", values="rating")
    return dfPivot

if __name__ == "__main__":
    print("Lets start V0.1.1")

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

    # prepare data
    df = prepare_data(df, nMostRated=100, nTopUser=100)

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

    # save data
    df.to_csv(args.output_path)
