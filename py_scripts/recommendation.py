import numpy as np
import pandas as pd
import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
from constants import numericColumns, lyricsAnalysisColumns
import os


MLP_MODEL_CACHE_FILE = "./model_cache/mlpSongsClassifier.joblib"
DT_MODEL_CACHE_FILE = "./model_cache/dtSongsClassifier.joblib"

def extractIndices(probabilityVector, N):
    return np.argpartition(probabilityVector[0], -N)[-N:]


def recommendN(songs, playlist, n, classifier = None, cache=None):
    if classifier is None:
        classifier = KNeighborsClassifier(n_neighbors=n)
    model = make_pipeline(
        StandardScaler(),
        classifier
    )
    songs[lyricsAnalysisColumns] = songs[lyricsAnalysisColumns].fillna(0)
    playlist[lyricsAnalysisColumns] = playlist[lyricsAnalysisColumns].fillna(0)

    songs_filtered = songs[numericColumns].dropna()
    X = songs_filtered[numericColumns]
    y = songs_filtered.index

    if cache is not None:
        try:
            model = load(cache)
        except:
            model.fit(X, y)
            dump(model, cache)
    else:
        model.fit(X,y)


    playlistVec = playlist[numericColumns].mean()
    playlistVec = pd.DataFrame(playlistVec).T
    probabilityVec = model.predict_proba(playlistVec)
    # print(probabilityVec[probabilityVec>0])
    indices = extractIndices(probabilityVec, n)
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

def exportRec(df, filename, suffix):
    df.to_csv('./recs/' + os.path.basename(filename).split(".")[0] + suffix, index=False)

def main(playlist, corpus, filename):
    numRecs = 5
    print("Recommending KNN")
    knnRecommendations = recommendN(corpus, playlist, numRecs)
    # svcRecommendations = recommendN(corpus, playlist, SVC(gamma=2))
    print("Recommending MLP")
    nnRecommendations = recommendN(corpus, playlist, numRecs, MLPClassifier(), cache=MLP_MODEL_CACHE_FILE)
    print("Recommending DT")
    rfRecommendations = recommendN(corpus, playlist, numRecs, DecisionTreeClassifier(min_samples_leaf=numRecs), cache=DT_MODEL_CACHE_FILE)
    exportRec(knnRecommendations, filename, "-knn.csv")
    exportRec(nnRecommendations, filename, "-nn.csv")
    exportRec(rfRecommendations, filename, "-dt.csv")
    return

if __name__ == "__main__":
    corpus = pd.read_csv("../spotifydata.csv")
    playlist = pd.read_csv(sys.argv[1])
    if len(sys.argv) == 3:
        corpus = pd.read_csv(sys.argv[2])
    main(playlist, corpus, sys.argv[1])
