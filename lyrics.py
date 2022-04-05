import pandas as pd
import numpy as np 
import sys
import nltk
import re 
import ast
from nltk.corpus import stopwords
from swaglyrics.cli import get_lyrics
from sklearn.feature_extraction.text import TfidfVectorizer
pd.options.mode.chained_assignment = None



def remove(text):
    removed = re.sub(r'(?:,|((\[)(Chorus|Verse(?:| [0-9]+)|Vers(?:| [0-9]+)|Bridge|Pre-Chorus|Post-Chorus|Outro|Intro|Interlude)(?:|: [^\]]*)(\]\n)))', "",text) 
    removed = removed.replace("(","").replace(")","")
    return removed


def filter_lyrics(playlist_row, cachedStopWords):
    
    lyrics = playlist_row['lyrics'][0]
    
    if lyrics is '' or lyrics is None:
        return 'Error: No lyrics found'
   
    # replace characters/words that are not a part of the lyrics with a space
    lyrics = remove(lyrics)
    
    # remove stopwords
    lyrics = ' '.join([word for word in lyrics.lower().split() if word not in cachedStopWords])
    
    return lyrics
    
    

    


def get_playlist_lyrics(row):
   
    song_name = row['song_name']
    artist = row['artist']
    print("Retriving lyrics for " + song_name + " by " + artist)
    
    lyrics = get_lyrics(song_name, artist)
    return [lyrics]
        

    
def main(playlist_csv):
            
    songs_df = pd.read_csv(playlist_csv)
    songs_df['lyrics'] = songs_df.apply(lambda row : get_playlist_lyrics(row), axis=1)
    
    print("Filtering lyrics ...")
    
    nltk.download('stopwords')
    cachedStopWords = stopwords.words("english")
#     songs_df['lyrics'] = songs_df['lyrics'].apply(ast.literal_eval)
    songs_df['lyrics_filtered'] = songs_df.apply(lambda row : filter_lyrics(row, cachedStopWords), axis=1)
    songs_df.to_csv("playlist.csv", index = False)
    
    print("Done")


if __name__ == '__main__':
    playlist_csv = sys.argv[1]
    main(playlist_csv)