import pandas as pd
import matplotlib.pyplot as plt

#df = pd.read_csv("data/coll_filt_data.csv")
df = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\merged_data_large.csv")

#df = df.head(10000)

pic_fold=r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Bilder\pyplots"

# count ratings per movie
plt.hist(df.rating, bins=10)
plt.title("Bewertungsverteilung")
plt.ylabel("Anzahl")
plt.xlabel("Bewertung")
plt.show()
plt.savefig(pic_fold+"/Bewertungsverteilung.png")

# count ratings per movie
plt.hist(sorted(df.groupby("movieId").count()["rating"], reverse=True), bins=20)
plt.title("Anzahl Bewertungen pro Film")
plt.ylabel("Anzahl Filme")
plt.xlabel("Anzahl Bewertungen")
plt.show()
plt.savefig(pic_fold+"/Anzahl Bewertungen pro Film.png")

vals = [x for x in sorted(df.groupby("movieId").count()["rating"], reverse=True) if x < 100]
plt.hist(vals, bins=20)
plt.title("Anzahl Bewertungen pro Film bis 100 Bewertungen")
plt.ylabel("Anzahl Filme")
plt.xlabel("Anzahl Bewertungen")
plt.show()
plt.savefig(pic_fold+"/Anzahl Bewertungen pro Film bis 100 Bewertungen.png")

# count ratings per user
plt.hist(sorted(df.groupby("userId").count()["rating"], reverse=True)[1:], bins=20)
plt.title("Anzahl Bewertungen pro User")
plt.ylabel("Anzahl User")
plt.xlabel("Anzahl Bewertungen")
plt.show()
plt.savefig(pic_fold+"/Anzahl Bewertungen pro User.png")

vals = [x for x in sorted(df.groupby("userId").count()["rating"], reverse=True) if x < 100]
plt.hist(vals, bins=20)
plt.title("Anzahl Bewertungen pro User bis 100 Bewertungen")
plt.ylabel("Anzahl User")
plt.xlabel("Anzahl Bewertungen")
plt.show()
plt.savefig(pic_fold+"/Anzahl Bewertungen pro User bis 100 Bewertungen.png")
