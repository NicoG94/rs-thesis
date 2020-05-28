from surprise import SVD, Dataset, Reader 
from surprise.model_selection import cross_validate
import pandas as pd

# Load the movielens-100k dataset (download it if needed).
data = Dataset.load_builtin('ml-100k')

# Load the movielens-100k dataset (download it if needed).
df = pd.read_csv("data/coll_filt_data.csv")

# take only top 1000 most rated movies
nMostRated = 100
mostRatedMovieIds = df.groupby("movieId").count().sort_values("userId", ascending = False).head(nMostRated).index

dfMostRated = df[df["movieId"].isin(mostRatedMovieIds)]

reader = Reader(rating_scale=(0, 5))
data = Dataset.load_from_df(dfMostRated.drop("timestamp", axis=1), reader)


# Use the famous SVD algorithm.
algo = SVD()

# Run 5-fold cross-validation and print results.
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

algo.predict(uid, iid)

def get_Iu(uid):
    """ return the number of items rated by given user
    args: 
      uid: the id of the user
    returns: 
      the number of items rated by the user
    """
    try:
        return len(trainset.ur[trainset.to_inner_uid(uid)])
    except ValueError: # user was not part of the trainset
        return 0
    
def get_Ui(iid):
    """ return number of users that have rated given item
    args:
      iid: the raw id of the item
    returns:
      the number of users that have rated the item.
    """
    try: 
        return len(trainset.ir[trainset.to_inner_iid(iid)])
    except ValueError:
        return 0
    
df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
df['Iu'] = df.uid.apply(get_Iu)
df['Ui'] = df.iid.apply(get_Ui)
df['err'] = abs(df.est - df.rui)
best_predictions = df.sort_values(by='err')[:10]
worst_predictions = df.sort_values(by='err')[-10:]