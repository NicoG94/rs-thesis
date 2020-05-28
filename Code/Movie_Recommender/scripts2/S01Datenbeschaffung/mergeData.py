import pandas as pd
import numpy as np 
import os
import scripts2.S01Datenbeschaffung.GoogleStorageQuery as gsq

head = None

# TODO: cont_based csv : imdbId als PrimärID

def convertImdbId(x):
    if np.isnan(x):
        return np.nan
    else:
        return "tt" + str(int(x))


def get_cont_base_filt_data():
    ### imdb
    basics = pd.read_csv(r"C:\Users\nicog\Desktop\thesis_daten\imdb\name.basics.tsv\data.tsv", sep='\t', header=0, nrows = head, na_values = r"\N", index_col="tconst")
    principals = pd.read_csv('principals.tsv', sep='\t', header=0, nrows = head, na_values = r"\N", index_col="tconst")
    ratings = pd.read_csv('ratings.tsv', sep='\t', header=0, nrows = head, na_values = r"\N", index_col="tconst")


    # group actors, directors etc to movie
    principalsGrouped = principals.groupby(principals.index)["nconst"].apply(list)

    basics.titleType.unique()
    movies = basics[(basics.titleType == "movie") | (basics.titleType == "tvMovie")]

    #idCol = "tconst"
    df = movies.join(principalsGrouped).join(ratings)
    imdb = df.rename(columns = {"nconst": "crew"})
    #df.to_csv("moviesRated.csv", index = False)


    ### grouplens
    tags = pd.read_csv("tags.csv", nrows = head, index_col = "movieId")
    links = pd.read_csv("links.csv", nrows = head, index_col = "movieId")

    # group tags
    tagsGrouped = tags.groupby(tags.index)["tag"].apply(list).to_frame()

    movielens = tagsGrouped.join(links)



    ### merge both
    # prepare imdbId col and set to index


    movielens["imdbId"] = movielens["imdbId"].apply(convertImdbId)
    movielens2 = movielens.set_index("imdbId")#[["tag"]]

    df2 = imdb.join(movielens2)
    print(len(df2) - df2.tag.isnull().sum())
    df3 = df2[df2.tag.notnull()]
    df3.to_csv(r"C:/Users/nicog/OneDrive/3. Semester - Masterthesis/Code/Movie_Recommender/data/cont_base_filt_data.csv", index = True)

### tmdb
# https://gist.github.com/galli-leo/6398f9128ffc20af70c6c7eedfeb0a65
# https://developers.themoviedb.org/3/getting-started/introduction
# https://www.themoviedb.org/documentation/api
# https://towardsdatascience.com/beginners-recommendation-systems-with-python-ee1b08d2efb6


# grouplens coll filt with imdb id
#def get_coll_filt_data() -> pd.DataFrame:
def get_coll_filt_data() -> str:

    # import functions for docker
    import pandas as pd
    import scripts2.S01Datenbeschaffung.GoogleStorageQuery as gsq

    # read data
    bucket_name = "movie_data_2603"
    links_file_name = "raw_data/links.csv"
    ratings_file_name = "raw_data/ratings.csv"

    links=gsq.read_csv(bucket_name, links_file_name)
    ratings=gsq.read_csv(bucket_name, ratings_file_name)

    # merge data
    ratingsImbd = ratings.merge(links,left_index=True, right_index=True)

    # upload data
    ratingsImbd.to_csv(r"C:/Users/nicog/OneDrive/3. Semester - Masterthesis/Code/Movie_Recommender/data/coll_filt_data.csv", index=False)
    upload_file_name = "prepared_data/coll_filt_data2.csv"
    gsq.write_csv(bucket_name, upload_file_name)

    print("coll_filt_data saved")
    #return ratingsImbd
    return "TestOutput"
