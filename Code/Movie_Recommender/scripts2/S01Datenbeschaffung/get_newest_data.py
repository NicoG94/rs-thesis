from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd


def main():
    url_file="ml-latest-small"
    url=f"http://files.grouplens.org/datasets/movielens/{url_file}.zip"
    resp = urlopen(url)
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.namelist()

    files=["links.csv", "ratings.csv"]
    for file in files:
        df = pd.read_csv(zipfile.open(f'{url_file}/{file}'))
        df.to_csv(f"gs://raw_movie_data/{file}")

if __name__ == "__main__":
    main()
