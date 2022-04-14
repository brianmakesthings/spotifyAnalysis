import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests, sys
import json
import ast

def get_onehot_encode(row, genres_length):
    np.set_printoptions(threshold=sys.maxsize)
    genre = row['genres_encoded']
    arr = np.zeros(5833)
    for item in genre:
        arr_genre = np.zeros(5833)
        arr_genre[item] = 1
        arr = np.row_stack((arr,arr_genre))
    return arr[1:]


def onehot_encode(playlist_df):
    
    with open("./img/genreList", "r") as fp:
        genreList = json.load(fp)
    
    genres_length = len(genreList)
    playlist_df['genres_encoded'] = playlist_df['genres_encoded'].apply(ast.literal_eval)
    playlist_df['genres_onehot_encoded'] = playlist_df.apply(lambda row : get_onehot_encode(row, genreList), axis=1)
    return playlist_df


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
