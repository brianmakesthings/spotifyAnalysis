import numpy as np
import pandas as pd
import plotly.express as px
import sys

def main(playlists, output=None):
    playlistDfs = list(map(lambda x: pd.read_csv(x, index_col=0).drop("Unnamed: 0", axis=1), playlists))
    numericColumns = ["danceability",
                    "energy",
                    "loudness",
                    "speechiness",
                    "acousticness",
                    "instrumentalness",
                    "liveness",
                    "valence",
                    "tempo"]
    # print(list(map(lambda x: x[numericColumns], playlistDfs)))
    # print([playlistDfs[0], playlistDfs[1]])
    comparisonDf = pd.concat(list(map(lambda x: x[numericColumns], playlistDfs)), keys=playlists) \
        .reset_index(1, drop=True) \
        .reset_index(col_fill='Source')
    fig = px.scatter_matrix(comparisonDf, 
        dimensions=numericColumns,
        color='index',
        width=1500,
        height=1500)
    fig.show()
    if output is not None:
        fig.write_html(output)
    return

if __name__ == "__main__":
    argc = len(sys.argv)
    if (argc < 2):
        print("Usage: python scatterplotMatrix.py [playlist1] [playlist2] ... [playlistN]")
    else:
        if (argc > 5):
            print("Many comparisons requested, visibility may be affected")
        main(sys.argv[1:])