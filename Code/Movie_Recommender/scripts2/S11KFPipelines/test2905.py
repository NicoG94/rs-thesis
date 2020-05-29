import pandas as pd
df = pd.DataFrame({"A":[5,6], "B":[1,2]})
print(df["A"].sum())
df.to_csv("./kfptestcsv.csv")