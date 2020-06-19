from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd

def data_validation(df, file):
    if file == "links.csv":
        assert list(df.columns)==["movieId", "imdbId", "tmdbId"]
    if file=="ratings.csv":
        assert list(df.columns) == ['userId', 'movieId', 'rating', 'timestamp']

def main(request):
    url_file="ml-latest-small"
    url=f"http://files.grouplens.org/datasets/movielens/{url_file}.zip"
    resp = urlopen(url)
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.namelist()

    files=["links.csv", "ratings.csv"]
    for file in files:
        df = pd.read_csv(zipfile.open(f'{url_file}/{file}'))
        try:
            data_validation(df, file)
        except AssertionError:
            print(f"{file} has wrong data format - please check!")
            return
        df.to_csv(f"gs://raw_movie_data/{file}")
    print("newest data uploaded")

if __name__ == "__main__":
    main({})
