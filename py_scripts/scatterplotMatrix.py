import numpy as np
import pandas as pd
import plotly.express as px
from constants import numericColumns
import sys

def plot(playlists, output=None, subdir=""):
    playlistDfs = list(map(lambda x: pd.read_csv(x), playlists))
    # print(list(map(lambda x: x[numericColumns], playlistDfs)))
    # print([playlistDfs[0], playlistDfs[1]])
    comparisonDf = pd.concat(list(map(lambda x: x[numericColumns], playlistDfs)), keys=playlists) \
        .reset_index(1, drop=True) \
        .reset_index(col_fill='Source')
    fig = px.scatter_matrix(comparisonDf, 
        dimensions=numericColumns,
        title=output,
        color='index',
        width=1900,
        height=1800)
    # fig.show()
    if output is not None:
        fig.write_html("img/scatterplotMatrix/" + subdir + output + ".html")
        fig.write_image("img/scatterplotMatrix/" + subdir + output + ".png")
    return

if __name__ == "__main__":
    argc = len(sys.argv)
    if (argc < 2):
        print("Usage: python scatterplotMatrix.py [playlist1] [playlist2] [title] [subdir?]")
    if (argc == 4):
        plot(sys.argv[1:3], sys.argv[3])
    elif (argc == 5):
        plot(sys.argv[1:3], sys.argv[3], sys.argv[4])
