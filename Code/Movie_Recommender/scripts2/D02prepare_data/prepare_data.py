import pandas as pd
import os
import logging
#from google.cloud import storage
import gcsfs
import argparse

def make_dir(temp_folder):
    # make folder and path
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

def prepare_data(df):
    df["AAA"] = pd.NA

def get_pd_path(bucket_name, file_name):
    pathToLinks = 'gs://{}/{}'.format(bucket_name, file_name)
    return pathToLinks

def read_csv(path):
    #path = get_pd_path(bucket_name, file_name)
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    print("Lets start V0.0.3")
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
    prepare_data(df)
    print("preparing done")


