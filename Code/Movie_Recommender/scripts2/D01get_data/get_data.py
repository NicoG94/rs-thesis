import pandas as pd
import argparse
from pathlib import Path

if __name__ == "__main__":
    print("Lets start V0.1.3")

    # get arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--output_path', type=str,
                        help='Path of the local file where the Output 1 data should be written.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--input_path_links', type=str,
                        help='Path of the local file containing the Input 1 data.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--input_path_ratings', type=str,
                        help='Path of the local file containing the Input 1 data.')  # Paths should be passed in, not hardcoded
    args = parser.parse_args()
    print(args)

    # read data
    ratings = pd.read_csv(args.input_path_ratings)
    links = pd.read_csv(args.input_path_links)

    # merge data
    ratingsImbd = ratings.merge(links, left_index=True, right_index=True)

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)

    # save data
    ratingsImbd.to_csv(args.output_path, index=False)
    print("DONE")
