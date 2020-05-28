

def train_algo(train_algo_test_param:str, test_output:str):
    # import functions for docker
    from surprise import SVD
    from surprise import Dataset
    from surprise import dump
    from surprise import Reader
    from surprise.model_selection import train_test_split

    import json
    import pandas as pd
    import scripts2.S01Datenbeschaffung.GoogleStorageQuery as gsq

    # Load the movielens-100k dataset (download it if needed).
    bucket_name = "movie_data_2603"
    coll_filt_file_name = "prepared_data/coll_filt_data2.csv"
    #df=gsq.read_csv(bucket_name, coll_filt_file_name)

    df = pd.read_csv("data/coll_filt_data.csv")

    # take only top 1000 most rated movies
    nMostRated = 100
    mostRatedMovieIds = df.groupby("imdbId").count().sort_values("userId", ascending = False).head(nMostRated).index

    dfMostRated = df[df["imdbId"].isin(mostRatedMovieIds)]
    dfMostRated["userId"] = dfMostRated["userId"].astype(str)
    dfMostRated["imdbId"] = dfMostRated["imdbId"].astype(str)

    reader = Reader(rating_scale=(1, 5))
    #df (Dataframe) – The d ataframe containing the ratings. It must have three columns, corresponding to the user (raw) ids, the item (raw) ids, and the ratings, in this order.
    data = Dataset.load_from_df(dfMostRated[["userId", "imdbId","rating"]], reader)

    #data.raw_ratings[0]

    trainset = data.build_full_trainset()

    #trainset, testset = train_test_split(data, test_size=.25)

    algo = SVD()
    algo.fit(trainset)

    # Compute predictions of the 'original' algorithm.
    predictions = algo.test(trainset.build_testset())

    '''
    # Dump algorithm and reload it.
    file_name = r"C:/Users/nicog/OneDrive/3. Semester - Masterthesis/Code/Movie_Recommender/models/simpleRS2.pkl"
    dump.dump(file_name, algo=algo)
    _, loaded_algo = dump.load(file_name)
    '''

    model_file_name = "models/simpleRS3"
    gsq.save_model(bucket_name, model_file_name, algo)

    loaded_algo = gsq.read_model(bucket_name, model_file_name)

    # We now ensure that the algo is still the same by checking the predictions.
    predictions_loaded_algo = loaded_algo.test(trainset.build_testset())
    assert predictions == predictions_loaded_algo
    print('Predictions are the same')


    uid = str(4094)  # raw user id (as in the ratings file). They are **strings**!
    iid = str(114709)  # raw item id (as in the ratings file). They are **strings**!

    pred = algo.predict(uid, iid, r_ui=4, verbose=True)
    print(pred)
    print("Algo trained and saved")
    with open('output.txt','w') as out_file:
        out_file.write(json.dumps("This worked"))
    #return algo

