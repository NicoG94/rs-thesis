import pandas as pd
import requests

links = pd.read_csv(r"C:\Users\nicog\Desktop\thesis_daten\grouplens\ml-latest\links.csv", index_col="imdbId")["tmdbId"]

df = pd.read_csv("data/coll_filt_data.csv")
# take only top 1000 most rated movies
nMostRated = 100
mostRatedMovieIdsImdb = df.groupby("imdbId").count().sort_values("userId", ascending = False).head(nMostRated).index
dfMostRated = df[df["imdbId"].isin(mostRatedMovieIdsImdb)]

def getDataFromTmdbApi(movieId):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=8a7e6043e512b2219a471b9bdfb78369'.format(movieId)

    resp = requests.get(url=url)
    data = resp.json()
    return data

def getImagePathFromMovie(data):
    try:
        imagePath = data["poster_path"]
        return imagePath
    except (KeyError, NameError) as e:
        print("{} has error: {}".format(movieId, e))
        return ""

def getTitleFromMovie(data):
    try:
        title = data["title"]
        return title
    except (KeyError, NameError) as e:
        print("{} has error: {}".format(movieId, e))
        return ""


popularMovies = dfMostRated[["imdbId","tmdbId"]].drop_duplicates()

movieData = {}
for movieId in popularMovies["tmdbId"]:
    movieData[movieId] = {}
    data = getDataFromTmdbApi(movieId)
    movieData[movieId]["posterPath"] = getImagePathFromMovie(data)
    movieData[movieId]["title"] = getTitleFromMovie(data)

movieDataDf = pd.DataFrame(movieData).transpose().reset_index()

popularMovies2 = popularMovies.merge(movieDataDf, left_on="tmdbId", right_on="index")

popularMovies2["imageurl"] = "http://image.tmdb.org/t/p/w1280" + popularMovies2["posterPath"]
popularMovies2.drop(["index","tmdbId","posterPath"],axis=1,inplace=True)
popularMovies2 = popularMovies2.rename(columns={'imdbId':"tconst", 'title': "moviename"})
popularMovies2[["imageurl", "moviename", "tconst"]].to_csv(r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Code\django_website\locallibrary\images.csv", index = False)


