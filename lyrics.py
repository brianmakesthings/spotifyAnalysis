import lyricsgenius
import pandas as pd


def get_lyrics(row, genius):
   
    song_name = row['song_name']
    artist = row['artist']
    
    song = genius.search_song(song_name, artist)
  
    if song is not None:
        return [song.lyrics]
    else:
        return "error: lyrics not found"


def get_playlist_lyrics(songs_df):
    
    # client_id = 'umj0FrQtvZaD4oYVzXUlHdWMVBjmhzsII6o0DkqV6any4f-chd0wkg8H-DYUslA8'
    # client_secret = 'TaPyqUGizzT4QUjJR85KTAYZ3TIU0JJvhbn015k2vnIeK9OmjugaWT0yJPKTcd6K_Pz3nf1XGk8xrtoAuU_-Rg'
    access_token = 'F2GrAfrqsHtMXLDY34yYFRjYktQ-vjtEAxam5S6sZt6pAItbbPaiQzl0Zqz_kpiR'
    genius = lyricsgenius.Genius(access_token)
    
    songs_df['lyrics'] = songs_df.apply(lambda row : get_lyrics(row, genius), axis=1)
    return songs_df