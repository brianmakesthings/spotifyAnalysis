import pandas as pd
import requests
import json
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# ----- import ------
# pip install spotipy
# setopt +o nomatch

# ----- how to run -----
# python3 playlist.py username playlist_id


def get_artist_genre(artist_id, sp):
    
    artist = sp.artist(artist_id)
    return artist["genres"]


def get_lyrics(artist, song):
    
    lyrics_url = 'https://api.lyrics.ovh/v1/' + artist + '/' + song
    result = requests.get(lyrics_url)
    
    if result.status_code in range(200, 299):
        lyrics = json.loads(result.content)
        return lyrics
    else:
        return {"error": "No lyrics found"}
    

def get_playlist(username, playlist_id, sp):
    
    song_feature_columns = ["danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness","liveness","valence","tempo", "type", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"]
    song_info_columns = ["song_name", "artist","album", "id", "artist_uri", "genres", "lyrics"]
   
    user_playlist_df = pd.DataFrame(columns = song_feature_columns + song_info_columns)
    playlist = sp.user_playlist_tracks(username, playlist_id)["items"]

    for song in playlist:     
       
        # stores all info of song 
        playlist_dict = {}
        
        playlist_dict["artist"] = song["track"]["album"]["artists"][0]["name"]
        playlist_dict["artist_uri"] = song["track"]["album"]["artists"][0]["uri"]
        playlist_dict["album"] = song["track"]["album"]["name"]
        playlist_dict["song_name"] = song["track"]["name"]
        playlist_dict["id"] = song["track"]["id"]
        
        # get genre of artist
        genres = get_artist_genre(playlist_dict["artist_uri"], sp)
        playlist_dict["genres"] = [genres]
        
        # get lyrics
        lyrics = get_lyrics(playlist_dict["artist"], playlist_dict["song_name"])
        playlist_dict["lyrics"] = [lyrics]
        
        # audio features
        audio_features = sp.audio_features(playlist_dict["id"])[0]  
        for feature in song_feature_columns:        
            playlist_dict[feature] = audio_features[feature]
        
        current_song = pd.DataFrame(playlist_dict)
        user_playlist_df = pd.concat([user_playlist_df, current_song], ignore_index = True)
        
    return user_playlist_df


def main():
    
    user_id = sys.argv[1]
    playlist_id = sys.argv[2]
    playlist_id = playlist_id.split('?si=')[0]
    
    client_id = '2ceb199cdce145b68b4b4fccca553198'
    client_secret = '962227d68ad54204b52d739fca6a1bfb'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
   
    playlist_df = get_playlist(user_id, playlist_id, sp)
    playlist_df.to_csv("playlist.csv")
    
    
if __name__ == '__main__':
    main()

# reference: https://towardsdatascience.com/how-to-create-large-music-datasets-using-spotipy-40e7242cc6a6


