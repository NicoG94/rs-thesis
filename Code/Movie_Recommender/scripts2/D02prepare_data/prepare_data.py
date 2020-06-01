import pandas as pd
import os
import logging
#from google.cloud import storage
import gcsfs

def make_dir(temp_folder):
    # make folder and path
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

def prepare_data(df):
    df["AAA"] = pd.NA

def get_pd_path(bucket_name, file_name):
    pathToLinks = 'gs://{}/{}'.format(bucket_name, file_name)
    return pathToLinks

def read_csv(bucket_name, file_name):
    path = get_pd_path(bucket_name, file_name)
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    print("Lets start")
    logging.info('getting the data...')
    #temp_folder = '/data_folder'
    #make_dir(temp_folder)
    bucket_name="movie_data_2603"
    file_name = "prepared_data/coll_filt_data_kfp_test.csv"
    df = read_csv(bucket_name, file_name)
    prepare_data(df)
    print("preparing done")

    r"""
    import argparse
    parser = argparse.ArgumentParser(description='Preprocessing')
    parser.add_argument('--data_bucket',
                        type=str,
                        help='GCS bucket where preprocessed data is saved',
                        default='abc')
    args = parser.parse_args()
    print(args.data_bucket)
    """
