import pandas as pd
import os
import logging

def make_dir(temp_folder):
    # make folder and path
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

def prepare_data(temp_folder):
    # get the data
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    file_path = os.path.join(temp_folder, 'data.csv')
    data = pd.read_csv(file_path)
    print(data)
    data["A"] = data["A"] + 10
    print(data)

if __name__ == "__main__":
    print("Lets start")
    logging.info('getting the data...')
    temp_folder = '/tmp'
    make_dir(temp_folder)
    prepare_data()

