import pandas as pd
import json

def get_data2():
    a = pd.DataFrame({"A":[1,2]})
    with open('output.txt','w') as out_file:
        out_file.write(json.dumps(a))
    return a


if __name__ == "__main__":
    b = get_data2()
    print(b)