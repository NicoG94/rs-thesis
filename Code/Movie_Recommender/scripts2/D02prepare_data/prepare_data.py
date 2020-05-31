import pandas as pd
import os
import logging

def make_dir(temp_folder):
    # make folder and path
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

def prepare_data(temp_folder):
    file_path = os.path.join(temp_folder, 'data.csv')
    #data = pd.read_csv(file_path)
    data = pd.DataFrame({"A":[1,2]})
    print(data)
    data["A"] = data["A"] + 10
    print(data)

if __name__ == "__main__":
    print("Lets start")
    logging.info('getting the data...')
    temp_folder = '/data_folder'
    make_dir(temp_folder)
    prepare_data(temp_folder)

