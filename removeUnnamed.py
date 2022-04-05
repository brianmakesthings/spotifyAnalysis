import pandas as pd
import sys

## removed unnamed column from older playlist csv files

def main(playlist_csv):

    playlist_df = pd.read_csv(playlist_csv)
    playlist_df = playlist_df.loc[:, ~playlist_df.columns.str.contains('^Unnamed')]
    playlist_df.to_csv(playlist_csv, index = False)
        

if __name__ == '__main__':
    playlist_csv = sys.argv[1]
    main(playlist_csv)