import os
import pandas as pd
from google.cloud import storage
from io import StringIO
import gcsfs
import pickle

#pathToCredentials = "data/storage_credentials.json"

def init_gs():
    #pathToCredentials = "storage_credentials.json"
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = pathToCredentials
    pass

def read_blob_gs(bucket_name, file_name):
    from google.cloud import storage
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)
    return blob

def read_gs_as_bytes_to_df(bucket_name, file_name, index_col=None):
    from google.cloud import storage
    import pandas as pd
    from io import StringIO

    blob = read_blob_gs(bucket_name, file_name)
    data = blob.download_as_string()

    s = str(data, 'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data, index_col=index_col)
    return df

def get_pd_path(bucket_name, file_name):
    pathToLinks = 'gs://{}/{}'.format(bucket_name, file_name)
    return pathToLinks

def read_csv(bucket_name, file_name):
    from google.cloud import storage
    import gcsfs
    import pandas as pd

    init_gs()
    path = get_pd_path(bucket_name, file_name)
    df = pd.read_csv(path)
    return df

def write_csv(df, bucket_name, file_name):
    from google.cloud import storage
    import gcsfs
    import pandas as pd

    init_gs()
    path = get_pd_path(bucket_name, file_name)
    df.to_csv(path)
    print(f"{file_name} saved to bucket {bucket_name}")

def save_model(bucket_name, file_name, algo):
    import gcsfs
    import pickle

    init_gs()
    fs = gcsfs.GCSFileSystem(project='rs-thesis')
    fs.ls(bucket_name)

    with fs.open(f'{bucket_name}/{file_name}', 'wb') as file:
        print(pickle.dump(algo, file))

    print(f"{file_name} saved to bucket {bucket_name}")

def read_model(bucket_name, file_name):
    import gcsfs
    import pickle

    init_gs()
    fs = gcsfs.GCSFileSystem(project='rs-thesis')
    fs.ls(bucket_name)

    with fs.open(f'{bucket_name}/{file_name}', 'rb') as file:
        loaded_algo = pickle.load(file)

    return loaded_algo
