import pandas as pd
from bs4 import BeautifulSoup
import requests, sys
import json
import ast


def encode_genre(row, genreList):
    genres = row['genres']
    
    genres_encoded = []
    
    for item in genres:
        index = genreList.index(item)
        genres_encoded.append(index)
    
    return genres_encoded


def main(playlist_csv):
    
    with open("genreList", "r") as fp:
        genreList = json.load(fp)
        
    playlist_df = pd.read_csv(playlist_csv)
    playlist_df['genres'] = playlist_df['genres'].apply(ast.literal_eval)
    playlist_df['genres_encoded'] = playlist_df.apply(lambda row : encode_genre(row, genreList), axis=1)

    playlist_df.to_csv(playlist_csv, index = False)
        

if __name__ == '__main__':
    playlist_csv = sys.argv[1]
    main(playlist_csv)