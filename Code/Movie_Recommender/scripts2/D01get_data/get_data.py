import os
from urllib.request import urlopen
from zipfile import ZipFile
#from google.cloud import storage
import gcsfs
import pandas as pd
import requests
import zipfile
import io
from datetime import date


def download_and_save_data(url, datafolder):
    r = requests.get(url, )
    zf = zipfile.ZipFile(io.BytesIO(r.content))

    #zipurl = url
    # Download the file from the URL
    #zipresp = urlopen(zipurl) # HIIIIER
    # Create a new file on the hard drive
    #tempzip = open("data_folder/tempfile.zip", "wb")
    # Write the contents of the downloaded file into the new file
    #tempzip.write(zipresp.read())
    # Close the newly-created file
    #tempzip.close()
    # Re-open the newly-created file with ZipFile()
    #zf = ZipFile("data_folder/tempfile.zip")
    # Extract its contents into <extraction_path>
    # note that extractall will automatically create the path
    zf.extractall(path='data_folder')
    # close the ZipFile instance
    #zf.close()

def make_dir(temp_folder):
    # make folder and path
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)


def read_csv(bucket_name, file_name):
    path = get_pd_path(bucket_name, file_name)
    data_downloaded = False
    while data_downloaded == False:
        try:
            df = pd.read_csv(path)
            data_downloaded = True
        except Exception as e:
            print(e)
    return df

def merge_data(bucket_name, links_file_name, ratings_file_name):

    links = read_csv(bucket_name, links_file_name)
    ratings = read_csv(bucket_name, ratings_file_name)

    # merge data
    ratingsImbd = ratings.merge(links, left_index=True, right_index=True)
    return ratingsImbd

def get_pd_path(bucket_name, file_name):
    pathToLinks = 'gs://{}/{}'.format(bucket_name, file_name)
    return pathToLinks

def write_csv(df, bucket_name, file_name):
    path = get_pd_path(bucket_name, file_name)
    df.to_csv(path)
    print(f"{file_name} saved to bucket {bucket_name}")

def get_data(temp_folder):
    print(temp_folder)
    a = pd.DataFrame({"A":[1,2]})
    file_path = os.path.join(
        temp_folder, 'data.csv')
    # save data
    a.to_csv(file_path, index=False)
    # save path
    with open("/blob_path.txt", "w") as output_file:
        output_file.write(file_path)


if __name__ == "__main__":
    print("Lets start V0.0.5")
    dataset = "ml-latest-small" # small
    #dataset = "ml-latest" # big
    bucket_name = "movie_data_2603"
    url = f"http://files.grouplens.org/datasets/movielens/{dataset}.zip"
    temp_folder = '/data_folder'
    today = date.today()
    today = "2020-06-01"

    links_file_name = f"raw_data/links_{dataset}_{today}.csv"
    ratings_file_name = f"raw_data/ratings_{dataset}_{today}.csv"

    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/out.json"

    #make_dir(temp_folder)
    #download_and_save_data(url, temp_folder)
    data = merge_data(bucket_name, links_file_name, ratings_file_name)

    output_file_name = "raw_data/coll_filt_data_kfp_{}.csv".format(today)

    write_csv(data, bucket_name, output_file_name)
    output_file_path = get_pd_path(bucket_name, output_file_name)
    # save path
    with open("/blob_path.txt", "w") as output_file:
        output_file.write(output_file_path)
    print("DONE")
