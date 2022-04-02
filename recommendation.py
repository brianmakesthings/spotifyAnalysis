import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier


numericColumns = ["danceability",
                  "energy",
                  "loudness",
                  "speechiness",
                  "acousticness",
                  "instrumentalness",
                  "liveness",
                  "valence",
                  "tempo"]

def extractIndices(probabilityVector, N):
    return np.argpartition(probabilityVector[0], -N)[-N:]


def recommendN(songs, playlist, n):
    model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier()
    )
    # print(playlist[["song_name", "artist"]])
    X = songs[numericColumns]
    y = songs.index
    model = KNeighborsClassifier(n_neighbors=n)
    model.fit(X, y)

    playlistVec = playlist[numericColumns].mean()
    playlistVec = pd.DataFrame(playlistVec).T
    probabilityVec = model.predict_proba(playlistVec)
    indices = extractIndices(probabilityVec, n)
    print(indices)
    print(songs.loc[indices])
    return songs.loc[indices]

# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.index
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
        ds = ds.batch(batch_size)
    return ds

def tensorRecommendN(songs, playlist, N):
    songs_ds = df_to_dataset(songs)
    # for feature_batch, label_batch in X_ds.take(1):
    #     print('Every feature:', list(feature_batch.keys()))
    #     print('A batch of targets:', label_batch)
    feature_columns = []
    for header in numericColumns:
        feature_columns.append(tf.feature_column.numeric_column(header))
    model = tf.keras.Sequential([
        # tf.keras.layers.Flatten(input_shape=X.values.shape),
        tf.keras.layers.DenseFeatures(feature_columns),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(len(songs))
    ])
    print("Starting Compilation of Tensorflow Model")
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(
                      from_logits=True),
                  metrics=['accuracy'])
    print("Starting Training of Tensorflow Model")
    model.fit(songs_ds, epochs=10)
    playlistVec = playlist[numericColumns].median()
    playlistVec = pd.DataFrame(playlistVec).T
    playlistVec_ds = df_to_dataset(playlistVec)

    probability_model = tf.keras.Sequential([model,
                                             tf.keras.layers.Softmax()])
    predictions = probability_model.predict(playlistVec_ds)
    top_n_indices = np.argpartition(predictions[0], -N)[-N:]
    print(songs.iloc[top_n_indices, ])


def test(songs, playlist, train_percent):
    database = pd.concat([songs, playlist])
    validation_set = playlist.sample(frac=1-train_percent, random_state=123)
    train_set = playlist.drop(validation_set.index)
    results = recommendN(database, train_set, int(
        (1-train_percent)*len(playlist)))
    recommendations = database.loc[list(results)]
    print(validation_set["song_name"])
    print(recommendations["song_name"])
    intersection = pd.merge(recommendations, validation_set, how="inner")
    print(len(intersection)/len(validation_set))


songs = pd.read_csv("./spotifydata.csv", index_col=0)
songs = songs.dropna()
playlist = pd.read_csv("./playlist.csv", index_col=0)
# songs = songs.set_index('id')
# playlist = playlist.set_index('id')
# test(playlist, 0.90)
recommendN(songs, playlist, 5)
# tensorRecommendN(songs, playlist, 5)
