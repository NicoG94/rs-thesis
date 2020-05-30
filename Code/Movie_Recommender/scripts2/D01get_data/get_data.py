import pandas as pd
import os
from urllib.request import urlopen
from zipfile import ZipFile

def download_and_save_data(url, datafolder):
    zipurl = url
    # Download the file from the URL
    zipresp = urlopen(zipurl)
    # Create a new file on the hard drive
    tempzip = open("data_folder/tempfile.zip", "wb")
    # Write the contents of the downloaded file into the new file
    tempzip.write(zipresp.read())
    # Close the newly-created file
    tempzip.close()
    # Re-open the newly-created file with ZipFile()
    zf = ZipFile("data_folder/tempfile.zip")
    # Extract its contents into <extraction_path>
    # note that extractall will automatically create the path
    zf.extractall(path='data_folder')
    # close the ZipFile instance
    zf.close()

def make_dir(temp_folder):
    # make folder and path
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

def merge_data(datafolder):
    links_file_name = f"{datafolder}/links.csv"
    ratings_file_name = f"{datafolder}/ratings.csv"

    links = pd.read_csv(links_file_name)
    ratings = pd.read_csv(ratings_file_name)

    # merge data
    ratingsImbd = ratings.merge(links, left_index=True, right_index=True)

    file_path = os.path.join(
        temp_folder, 'data.csv')

    # upload data
    ratingsImbd.to_csv(file_path, index=False)

    # save data
    ratingsImbd.to_csv(file_path, index=False)
    # save path
    with open("blob_path.txt", "w") as output_file:
        output_file.write(file_path)

def get_data2(temp_folder):
    a = pd.DataFrame({"A":[1,2]})


    file_path = os.path.join(
        temp_folder, 'data.csv')
    # save data
    a.to_csv(file_path, index=False)
    # save path
    with open("/blob_path.txt", "w") as output_file:
        output_file.write(file_path)


if __name__ == "__main__":
    # url = "http://files.grouplens.org/datasets/movielens/ml-latest.zip" # big
    #url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    temp_folder = '/data_folder'
    make_dir(temp_folder)
    #download_and_save_data(url, temp_folder)
    #merge_data(temp_folder)

    get_data2(temp_folder)


