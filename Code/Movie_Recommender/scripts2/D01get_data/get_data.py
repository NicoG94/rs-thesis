import pandas as pd

def get_data2():
    a = pd.DataFrame({"A":[1,2]})
    return a


if __name__ == "__main__":
    b = get_data2()
    print(b)