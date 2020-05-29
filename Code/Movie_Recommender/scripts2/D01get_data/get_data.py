import pandas as pd

a = pd.DataFrame({"A":[1,2]})
print(a)
print("print success")
a.to_csv("csv_test_success.csv")

f = open("requirements.txt")
print(f.read())

import numpy as np
b = np.array([0,1])
print(b)

import kfp