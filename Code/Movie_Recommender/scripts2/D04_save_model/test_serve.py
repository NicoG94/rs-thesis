from sklearn import svm
from sklearn import datasets
#from joblib import dump
import os
from sklearn.externals.joblib import dump
clf = svm.SVC(gamma='scale')
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf.fit(X, y)
dump(clf, 'model.joblib')
file_mb = os.stat("model.joblib").st_size/1000000
print(file_mb)
#python -m sklearnserver --model_dir model.joblib --model_name svm
#python -m sklearnserver --model_dir C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\model.joblib --model_name svm

# predict
from sklearn import datasets
import requests
iris = datasets.load_iris()
X, y = iris.data, iris.target
formData = {
    'instances': X[0:1].tolist()
}
res = requests.post('http://localhost:8080/v1/models/svm:predict', json=formData)
print(res)
print(res.text)


import os
model_path=r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\model.joblib"
MODEL_BASENAME = "model"
MODEL_EXTENSIONS = [".joblib", ".pkl", ".pickle"]
paths = [os.path.join(model_path, MODEL_BASENAME + model_extension)
                 for model_extension in MODEL_EXTENSIONS]
model_file = next(path for path in paths if os.path.exists(path))
[path for path in paths if os.path.exists(path)]


from joblib import load
algo_skl = load(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\model.joblib")
algo=load(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data_folder\simpleRS.joblib")
uid = str(4094)  # raw user id (as in the ratings file). They are **strings**!
iid = str(114709)  # raw item id (as in the ratings file). They are **strings**!
pred = algo.predict(uid, iid, r_ui=4, verbose=True)
print(pred[3])
