import pandas as pd
import os
import logging
#from google.cloud import storage
import gcsfs
import argparse
from datetime import date

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
    print("Lets start V0.0.4")
    logging.info('getting the data...')
    #temp_folder = '/data_folder'
    #make_dir(temp_folder)
    parser = argparse.ArgumentParser(description='Preprocessing')
    parser.add_argument('--blob_path',
                        type=str,
                        help='GCS path where raw data is saved')
    args = parser.parse_args()
    print(args.blob_path)
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


