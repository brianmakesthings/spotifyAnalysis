import pandas as pd
import requests
import json
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyrics import get_playlist_lyrics
from songReleaseDate import songReleaseDate


# ----- import ------
# pip install spotipy
# pip install swaglyrics
# setopt +o nomatch

# ------ inputs ------
# python3 playlist.py username playlist_id

def get_artist_genre(artist_id, sp):
    
    artist = sp.artist(artist_id)
    return artist["genres"]
    

def get_playlist(username, playlist_id, sp):
    
    song_feature_columns = ["danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness","liveness","valence","tempo", "type", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"]
    song_info_columns = ["song_name", "artist","album", "id", "artist_uri", "genres", "lyrics"]
   
    user_playlist_df = pd.DataFrame(columns = song_feature_columns + song_info_columns)
    playlist = sp.user_playlist_tracks(username, playlist_id)["items"]

    count = 0

    for song in playlist: 
     
        print("fetching song", count)
        count = count + 1    
       
        # stores all info of song 
        playlist_dict = {}
        
        playlist_dict["artist"] = song["track"]["album"]["artists"][0]["name"]
        playlist_dict["artist_uri"] = song["track"]["album"]["artists"][0]["uri"]
        playlist_dict["album"] = song["track"]["album"]["name"]
        playlist_dict["song_name"] = song["track"]["name"]
        playlist_dict["id"] = song["track"]["id"]
        playlist_dict["popularity"] = song["track"]["popularity"]
        songReleaseDate(song, playlist_dict)
        
        # get genre of artist
        genres = get_artist_genre(playlist_dict["artist_uri"], sp)
        playlist_dict["genres"] = [genres]
        
        # audio features
        audio_features = sp.audio_features(playlist_dict["id"])[0]  
        for feature in song_feature_columns:        
            playlist_dict[feature] = audio_features[feature]
        
        current_song = pd.DataFrame(playlist_dict)
        user_playlist_df = pd.concat([user_playlist_df, current_song], ignore_index = True)
        
    return user_playlist_df


def main(user_id, playlist_id, output_file):
    
    user_id = sys.argv[1]
    playlist_id = sys.argv[2]
    playlist_id = playlist_id.split('?si=')[0]
    
    client_id = '2ceb199cdce145b68b4b4fccca553198'
    client_secret = '962227d68ad54204b52d739fca6a1bfb'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
   
    playlist_df = get_playlist(user_id, playlist_id, sp)
    playlist_df.to_csv(output_file, index = False)
    
if __name__ == '__main__':
    user_id = sys.argv[1]
    playlist_id = sys.argv[2]
    output_file = sys.argv[3]
    main(user_id, playlist_id, output_file)

# reference: https://towardsdatascience.com/how-to-create-large-music-datasets-using-spotipy-40e7242cc6a6