import pandas as pd
import matplotlib.pyplot as plt
import os
os.chdir(r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Thesis\Code\Movie_Recommender")
#df = pd.read_csv("data/coll_filt_data.csv")
df = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\merged_data.csv")

df = df.head(10000)

# verteilung rating
df.rating.hist()

# count ratings per movie
plt.plot(sorted(df.groupby("movieId").count()["rating"], reverse=True))
plt.show()

# count ratings per user
plt.plot(sorted(df.groupby("userId").count()["rating"], reverse=True))
plt.show()

