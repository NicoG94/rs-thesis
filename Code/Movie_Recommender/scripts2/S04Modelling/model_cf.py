#https://towardsdatascience.com/prototyping-a-recommender-system-step-by-step-part-1-knn-item-based-collaborative-filtering-637969614ea 
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import load_npz

spmatrix = load_npz("data/coll_filt_sparse_matrix.npz")


spmatrix.count_nonzero()

# how many values are > 0?


# knn
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model_knn.fit(spmatrix)
distances, indices = model_knn.kneighbors(
            spmatrix[[5,10,15]],
            n_neighbors=10+1)

# get list of raw idx of recommendations
raw_recommends = \
    sorted(
        list(
            zip(
                indices.squeeze().tolist(),
                distances.squeeze().tolist()
            )
        ),
        key=lambda x: x[1]
    )[:0:-1]
    
    
# matrix factorization
    
    
    