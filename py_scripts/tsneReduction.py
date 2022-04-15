import sys
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.manifold import TSNE
from constants import numericColumns, metaDataColumns

def main(output, playlists):
    playlistDfs = list(map(lambda x: pd.read_csv(x).dropna(), playlists))
    comparisonDf = pd.concat(list(map(lambda x: x[numericColumns + metaDataColumns], playlistDfs)), keys=playlists) \
        .reset_index(1, drop=True) \
        .reset_index(col_fill='Source')
    print(comparisonDf)
    tsne = TSNE(perplexity=30, n_iter=500)
    # tsne = TSNE()
    reduced = tsne.fit_transform(comparisonDf[numericColumns])
    reducedDf = pd.DataFrame(reduced)
    reducedDf["source"] = comparisonDf["index"]
    reducedDf[metaDataColumns] = comparisonDf[metaDataColumns]
    print(reducedDf)
    fig = px.scatter(reducedDf, x=0, y=1, color="source", hover_data=metaDataColumns)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.write_html(output+".html")
    fig.write_image(output+".png")
    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])