import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

songs = pd.read_csv("./spotifydata.csv", index_col=0)
# songs.head()
songs = songs.dropna()

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
model = KNeighborsClassifier()
scaler.fit(songs[numericColumns])
X = scaler.transform(songs[numericColumns])
y = songs["id"]
model.fit(X, y)

playlist = pd.read_csv("./playlist.csv", index_col=0)
playlistVec = playlist[numericColumns].mean()
playlistVec = pd.DataFrame(playlistVec).T
playlistVec = scaler.transform(playlistVec)
# print(playlistVec.dtypes)
distances, indices = model.kneighbors(playlistVec, n_neighbors=5)
print(songs.iloc[indices[0]])

# print(songs[songs["id"] == pred[0]])
