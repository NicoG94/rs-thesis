# Code/Movie_Recommender/scripts2/D06_predict/Dockerfile
import pandas as pd
import argparse
from pathlib import Path


if __name__ == "__main__":
    print("Lets start V0.1.5")

    df = pd.read_csv("gcp_data/rs_predictions/prepared_data.csv")
    print(df.head())
