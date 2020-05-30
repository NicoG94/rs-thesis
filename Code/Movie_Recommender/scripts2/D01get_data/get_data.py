import pandas as pd
import json
import requests
import os

#def get_ratings():


#def get_links():


def get_data2():
    a = pd.DataFrame({"A":[1,2]})

    # make folder and path
    temp_folder = 'data'
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    file_path = os.path.join(
        temp_folder, 'data.csv')
    # save data
    a.to_csv(file_path, index=False)
    # save path
    with open("blob_path.txt", "w") as output_file:
        output_file.write(file_path)


if __name__ == "__main__":
    get_data2()