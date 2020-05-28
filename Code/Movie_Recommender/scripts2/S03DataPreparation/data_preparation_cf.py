import pandas as pd
from scipy.sparse import csr_matrix, save_npz

df = pd.read_csv("data/coll_filt_data.csv")

# take only top 1000 most rated movies
nMostRated = 100
mostRatedMovieIds = df.groupby("movieId").count().sort_values("userId", ascending = False).head(nMostRated).index

dfMostRated = df[df["movieId"].isin(mostRatedMovieIds)]

def createSparseMatrix(df, rowCol, colCol, valCol):
    '''
    Original row & col value will be substracted with 1, e.g. original rowCol value == 1 -> matrix row value == 0
    '''
    user_u = list(sorted(df[colCol].unique()))
    movie_u = list(sorted(df[rowCol].unique()))
    
    data = df[valCol].tolist()
    col = df[colCol].astype('category').cat.codes#, categories=user_u).cat.codes
    row = df[rowCol].astype('category').cat.codes#, categories=movie_u).cat.codes
    try:
        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(movie_u)))
    except ValueError:
        sparse_matrix = csr_matrix((data, (col, row)), shape=(len(user_u), len(movie_u)))
        sparse_matrix = sparse_matrix.transpose()
    return sparse_matrix

#pivot the dataframe to the wide format with movies as rows and users as columns
sparse_matrix = createSparseMatrix(df=df, rowCol="movieId", colCol = "userId", valCol = "rating")
save_npz("data/coll_filt_sparse_matrix.npz", sparse_matrix)
# did not work: 
#sparse_matrix = df.pivot(index='movieId',columns='userId',values='rating')

