import numpy as np
import pandas as pd
import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from joblib import dump, load


numericColumns = ["danceability",
                  "energy",
                  "loudness",
                  "speechiness",
                  "acousticness",
                  "instrumentalness",
                  "liveness",
                  "valence",
                  "tempo"]

MLP_MODEL_CACHE_FILE = "./mlpSongsClassifier.joblib"

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

def nnRecommendN(songs, playlist, n):
    X = songs[numericColumns]
    y = songs.index

    model = make_pipeline(
        StandardScaler(),
        MLPClassifier(),
    )

    try:
        model = load(MLP_MODEL_CACHE_FILE)
    except:
        model.fit(X,y)
        dump(model, MLP_MODEL_CACHE_FILE)

    playlistVec = playlist[numericColumns].mean()
    playlistVec = pd.DataFrame(playlistVec).T
    probabilityVec = model.predict_proba(playlistVec)
    indices = extractIndices(probabilityVec, n)
    print(indices)
    print(songs.loc[indices])
    return songs.loc[indices]


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

def main(playlist, corpus):
    nnRecommendN(corpus, playlist, 5)
    return

if __name__ == "__main__":
    corpus = pd.read_csv("./spotifydata.csv", index_col=0)
    playlist = pd.read_csv(sys.argv[1], index_col=0)
    if len(sys.argv) == 3:
        corpus = pd.read_csv(sys.argv[2], index_col=0)
    main(playlist, corpus)
