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
    df["AAA"] = pd.NA
    # take only top 1000 most rated movies

    mostRatedMovieIds = df.groupby("imdbId").count().sort_values("userId", ascending=False).head(nMostRated).index

    dfMostRated = df[df["imdbId"].isin(mostRatedMovieIds)]

    mostRatedUserIds = df.groupby("userId").count().sort_values("rating", ascending=False)[10:nTopUser + 10].index

    dfMostRated2 = dfMostRated[dfMostRated["userId"].isin(mostRatedUserIds)]

    dfPivot = dfMostRated2.pivot(index="userId", columns="imdbId", values="rating")
    return dfPivot

if __name__ == "__main__":
    print("Lets start V0.1.0")
    r"""
    #temp_folder = '/data_folder'
    #make_dir(temp_folder)
    parser = argparse.ArgumentParser(description='Preprocessing')
    parser.add_argument('--blob_path',
                        type=str,
                        help='GCS path where raw data is saved')
    args = parser.parse_args()
    print(args.blob_path)
    b = pd.read_csv(args.blob_path)
    print(b)
    
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/out.json"
    df = read_csv(args.blob_path)
    dfPivot = prepare_data(df)

    today = date.today()
    today = "2020-06-01"
    bucket_name = "movie_data_2603"
    output_file_name = "prepared_data/coll_filt_data_kfp_pivoted_{}.csv".format(today)

    write_csv(dfPivot, bucket_name, output_file_name)
    # get_data(temp_folder)
    output_file_path = get_pd_path(bucket_name, output_file_name)
    # save path
    with open("/blob_path.txt", "w") as output_file:
        output_file.write(output_file_path)
    print("DONE")
    """

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--input1-path', type=str,
                        help='Path of the local file containing the Input 1 data.')  # Paths should be passed in, not hardcoded
    #parser.add_argument('--param1', type=int, default=100, help='Parameter 1.')
    parser.add_argument('--output1-path', type=str,
                        help='Path of the local file where the Output 1 data should be written.')  # Paths should be passed in, not hardcoded
    args = parser.parse_args()
    print(args)
    print(args.input1_path)
    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

    #df = str_to_df(args.input1_path)
    #print(df)

    #with open(args.input1_path, 'r') as input1_file:
    with open(args.output1_path, 'w') as output1_file:
        output1_file.write("This was a success")

    df = pd.read_csv(args.input1_path)
