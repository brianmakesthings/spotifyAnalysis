import sys
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.manifold import TSNE

# def tsneReduce(playlists):
numericColumns = ["danceability",
                "energy",
                "loudness",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "liveness",
                "valence",
                "tempo",
                ]

def main(playlists):
    playlistDfs = list(map(lambda x: pd.read_csv(x, index_col=0).drop("Unnamed: 0", axis=1).dropna(), playlists))
    comparisonDf = pd.concat(list(map(lambda x: x[numericColumns], playlistDfs)), keys=playlists) \
        .reset_index(1, drop=True) \
        .reset_index(col_fill='Source')
    print(comparisonDf)
    tsne = TSNE(perplexity=5, n_iter=5000)
    reduced = tsne.fit_transform(comparisonDf[numericColumns])
    reducedDf = pd.DataFrame(reduced)
    reducedDf["source"] = comparisonDf["index"]
    fig = px.scatter(x=reducedDf[0], y=reducedDf[1], color=reducedDf["source"])
    fig.show()
    return

if __name__ == "__main__":
    main(sys.argv[1:])