import pandas as pd
import argparse
from pathlib import Path

def train_model(df):
    return "yeah"

if __name__ == "__main__":
    print("Lets start V0.1.2")

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

    # train model
    model = train_model(df)

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

    # save model
    model_path = args.output1_path+"/sample.txt"
    text_file = open(model_path, "wt")
    n = text_file.write(model)
    text_file.close()
