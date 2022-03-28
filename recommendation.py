import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def recommendN(songs, playlist, n):

    numericColumns = ["danceability",
                      "energy",
                      "loudness",
                      "speechiness",
                      "acousticness",
                      "instrumentalness",
                      "liveness",
                      "valence",
                      "tempo"]
    # model = make_pipeline(
    #     StandardScaler(),
    #     KNeighborsClassifier()
    # )
    scaler = StandardScaler()
    scaler.fit(songs[numericColumns])
    X = scaler.transform(songs[numericColumns])
    y = songs.index
    model = KNeighborsClassifier(n_neighbors=len(X))
    model.fit(X, y)

    playlistVec = playlist[numericColumns].median()
    playlistVec = pd.DataFrame(playlistVec).T
    playlistVec = scaler.transform(playlistVec)
    # print(playlistVec.dtypes)
    distances, indices = model.kneighbors(playlistVec, n_neighbors=n)
    return songs.iloc[indices[0]].index


def test(playlist, train_percent):
    p = playlist.set_index('id')
    s = songs.set_index('id')
    database = pd.concat([s, p])
    validation_set = p.sample(frac=1-train_percent, random_state=123)
    train_set = p.drop(validation_set.index)
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
test(playlist, 0.90)
