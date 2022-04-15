import pandas as pd
import requests
import json
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyrics import get_playlist_lyrics
from songReleaseDate import songReleaseDate
import time


# ----- import ------
# pip install spotipy
# pip install swaglyrics
# setopt +o nomatch

# ------ inputs ------
# python3 playlist.py username playlist_id

song_feature_columns = ["danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness","liveness","valence","tempo", "type", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"]
song_info_columns = ["song_name", "artist","album", "id", "artist_uri", "genres", "lyrics"]

def get_artist_genre(artist_id, sp):
    
    try:
        artist = sp.artist(artist_id)
    except:
        time.sleep(5)
        artist = sp.artist(artist_id)
    return artist["genres"]

def update_corpus(sp, path):
    corpus = pd.read_csv(path)
    corpus_res_df = pd.DataFrame(columns = song_feature_columns + song_info_columns)
    pos = 1
    count = len(corpus)

    for _, track in corpus.iterrows():
        print("fetching song", pos, "/", count)
        pos = pos + 1    
        try:
            song = sp.track(track["id"])
        except:
            time.sleep(5)
            song = sp.track(track["id"])
       
        # stores all info of song 
        playlist_dict = {}
        
        playlist_dict["artist"] = song["album"]["artists"][0]["name"]
        playlist_dict["artist_uri"] = song["album"]["artists"][0]["uri"]
        playlist_dict["album"] = song["album"]["name"]
        playlist_dict["song_name"] = song["name"]
        playlist_dict["id"] = song["id"]
        playlist_dict["popularity"] = song["popularity"]
        playlist_dict["release_date"] = song["album"]["release_date"]
        
        # get genre of artist
        genres = get_artist_genre(playlist_dict["artist_uri"], sp)
        playlist_dict["genres"] = [genres]
        
        # audio features
        # audio_features = sp.audio_features(playlist_dict["id"])[0]  
        for feature in song_feature_columns:        
            playlist_dict[feature] = track[feature]
        
        current_song = pd.DataFrame(playlist_dict)
        corpus_res_df = pd.concat([corpus_res_df, current_song], ignore_index = True)
    
    return corpus_res_df
    

def main(path="../spotifydata.csv"):
    
    client_id = '2ceb199cdce145b68b4b4fccca553198'
    client_secret = '962227d68ad54204b52d739fca6a1bfb'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
   
    playlist_df = update_corpus(sp, path)
    playlist_df.to_csv(path, index = False)
    
if __name__ == '__main__':
    main()

# reference: https://towardsdatascience.com/how-to-create-large-music-datasets-using-spotipy-40e7242cc6a6