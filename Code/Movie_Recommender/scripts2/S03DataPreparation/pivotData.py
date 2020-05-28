import pandas as pd
import scripts2.S01Datenbeschaffung.GoogleStorageQuery as gsq

def get_pivot_data():
    # import functions for docker
    import pandas as pd
    import scripts2.S01Datenbeschaffung.GoogleStorageQuery as gsq

    # read data
    bucket_name = "movie_data_2603"
    coll_filt_file_name = "prepared_data/coll_filt_data2.csv"
    df=gsq.read_csv(bucket_name, coll_filt_file_name)

    # take only top 1000 most rated movies
    nMostRated = 100
    mostRatedMovieIds = df.groupby("imdbId").count().sort_values("userId", ascending = False).head(nMostRated).index

    dfMostRated = df[df["imdbId"].isin(mostRatedMovieIds)]

    nTopUser=100
    mostRatedUserIds = df.groupby("userId").count().sort_values("rating", ascending = False)[10:nTopUser+10].index

    dfMostRated2 = dfMostRated[dfMostRated["userId"].isin(mostRatedUserIds)]

    dfPivot = dfMostRated2.pivot(index = "userId", columns="imdbId", values="rating")

    # upload data
    upload_file_name = "prepared_data/pivotedRatings2.csv"
    gsq.write_csv(bucket_name, upload_file_name)

    print("pivoted data saved")
    #return dfPivot
