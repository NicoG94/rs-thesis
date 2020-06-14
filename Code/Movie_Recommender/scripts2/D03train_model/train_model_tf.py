# https://towardsdatascience.com/building-a-collaborative-filtering-recommender-system-with-tensorflow-82e63d27b420

import pandas as pd
import argparse
from pathlib import Path
from sklearn.externals.joblib import dump
import os

def train_model_and_predict(df, user_col="userId", item_col="imdbId", rating_col="rating"):
    scaler = MinMaxScaler()
    df[rating_col] = df[rating_col].values.astype(float)
    rating_scaled = pd.DataFrame(scaler.fit_transform(df[rating_col].values.reshape(-1, 1)))
    df[rating_col] = rating_scaled

    df = df.drop_duplicates([user_col, item_col])
    user_book_matrix = df.pivot(index=user_col, columns=item_col, values=rating_col)
    user_book_matrix.fillna(0, inplace=True)
    users = user_book_matrix.index.tolist()
    books = user_book_matrix.columns.tolist()
    user_book_matrix = user_book_matrix.values

    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()

    num_input = df[item_col].nunique()
    num_hidden_1 = 10
    num_hidden_2 = 5

    X = tf.placeholder(tf.float64, [None, num_input])

    weights = {
        'encoder_h1': tf.Variable(tf.random_normal([num_input, num_hidden_1], dtype=tf.float64)),
        'encoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_hidden_2], dtype=tf.float64)),
        'decoder_h1': tf.Variable(tf.random_normal([num_hidden_2, num_hidden_1], dtype=tf.float64)),
        'decoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_input], dtype=tf.float64)),
    }

    biases = {
        'encoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
        'encoder_b2': tf.Variable(tf.random_normal([num_hidden_2], dtype=tf.float64)),
        'decoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
        'decoder_b2': tf.Variable(tf.random_normal([num_input], dtype=tf.float64)),
    }

    def encoder(x):
        layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']), biases['encoder_b1']))
        layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']), biases['encoder_b2']))
        return layer_2

    def decoder(x):
        layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']), biases['decoder_b1']))
        layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']), biases['decoder_b2']))
        return layer_2

    encoder_op = encoder(X)
    decoder_op = decoder(encoder_op)
    y_pred = decoder_op
    y_true = X

    loss = tf.losses.mean_squared_error(y_true, y_pred)
    optimizer = tf.train.RMSPropOptimizer(0.03).minimize(loss)
    eval_x = tf.placeholder(tf.int32, )
    eval_y = tf.placeholder(tf.int32, )
    pre, pre_op = tf.metrics.precision(labels=eval_x, predictions=eval_y)

    # Add an op to initialize the variables.
    init = tf.global_variables_initializer()
    local_init = tf.local_variables_initializer()
    pred_data = pd.DataFrame()

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()

    with tf.Session() as session:
        epochs = 100
        batch_size = 35

        session.run(init)
        session.run(local_init)

        num_batches = int(user_book_matrix.shape[0] / batch_size)
        user_book_matrix = np.array_split(user_book_matrix, num_batches)

        for i in range(epochs):

            avg_cost = 0
            for batch in user_book_matrix:
                _, l = session.run([optimizer, loss], feed_dict={X: batch})  # actual train/fit
                avg_cost += l

            avg_cost /= num_batches

            print("epoch: {} Loss: {}".format(i + 1, avg_cost))

        # Save the variables to disk.
        save_path = saver.save(session, "model.ckpt")
        print("Model saved in path: %s" % save_path)

        user_book_matrix = np.concatenate(user_book_matrix, axis=0)

        preds = session.run(decoder_op, feed_dict={X: user_book_matrix})

        pred_data = pred_data.append(pd.DataFrame(preds))

        pred_data = pred_data.stack().reset_index(name=item_col)
        pred_data.columns = [user_col, item_col, rating_col]
        pred_data[user_col] = pred_data[user_col].map(lambda value: users[value])
        pred_data[item_col] = pred_data[item_col].map(lambda value: books[value])

    print("Algo trained")
    return pred_data

if __name__ == "__main__":
    # WALS collaborative filtering model
    # Weighted Alternating Least Squares
    print("Lets start V0.1.5")

    # get arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--output_path', type=str,
                        help='Path of the local file where the Output 1 data should be written.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--input_path', type=str,
                        help='Path of the local file containing the Input 1 data.')  # Paths should be passed in, not hardcoded
    parser.add_argument('--make_cv', type=str,
                        help='If cross validation shall be applied')  # Paths should be passed in, not hardcoded
    parser.add_argument('--make_train_test_split', type=str,
                        help='If testset shall be created')  # Paths should be passed in, not hardcoded
    args = parser.parse_args()
    print(args)

    # read data
    # index="userId", columns="imdbId", values="rating"
    df = pd.read_csv(args.input_path).head(1000)
    #df = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\merged_data.csv").head(1000)


    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from sklearn.preprocessing import MinMaxScaler

    df_orig = pd.read_csv(r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data\merged_data.csv").head(1000)
    df = df_orig[["userId", "imdbId", "rating"]]
    user_col = "userId"
    item_col = "imdbId"
    rating_col = "rating"
    # only keep movies&users with > 20 ratings


    # train model
    print("start training")
    pred_data = train_model_and_predict(df)

    keys = [user_col, item_col]
    index_1 = pred_data.set_index(keys).index
    index_2 = df.set_index(keys).index

    top_ten_ranked = pred_data[~index_1.isin(index_2)]
    top_ten_ranked = top_ten_ranked.sort_values([user_col, item_col], ascending=[True, False])
    top_ten_ranked = top_ten_ranked.groupby(user_col).head(10)

    top_ten_ranked.loc[top_ten_ranked[user_col] == 1]

    df.loc[df[user_col] == 1].sort_values(by=[rating_col], ascending=False)


    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)

    # save model
    #path=r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data_folder\model.joblib"
    dump(model, args.output_path, compress=3)
    print("model saved")

    file_mb = os.stat(args.output_path).st_size / 1000000
    print(f"Model has {file_mb} MB.")