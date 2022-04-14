import sys
import pandas as pd
from scipy.stats import ttest_ind

numericColumns = ["danceability",
                  "energy",
                  "loudness",
                  "speechiness",
                  "acousticness",
                  "instrumentalness",
                  "liveness",
                  "valence",
                  "tempo"]

def compareMeans(df1, df2, columns = numericColumns):
    results = []
    for col in columns:
        # print(df1[col].mean(), df2[col].mean())
        _, pvalue = ttest_ind(df1[col], df2[col])
        results.append({"col_name": col, 
                        "p_val": pvalue,
                        "mean_1": df1[col].mean(),
                        "mean_2": df2[col].mean()})
    return pd.DataFrame(results)
def main(playlist1, playlist2):
    df1 = pd.read_csv(playlist1)
    df2 = pd.read_csv(playlist2).dropna()
    meanComparison = compareMeans(df1, df2)
    print(meanComparison)
    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])