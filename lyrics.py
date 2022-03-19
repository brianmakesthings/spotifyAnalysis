import pandas as pd
import numpy as np 
import sys
import nltk
import re 
import ast
from nltk.corpus import stopwords
from swaglyrics.cli import get_lyrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer



def remove(text):
    removed = re.sub(r'(?:,|((\[)(Chorus|Verse(?:| [0-9]+)|Bridge|Pre-Chorus|Post-Chorus|Outro)(?:|: [^\]]*)(\]\n)))', "",text) 
    removed = re.sub(r"(\n\n)+", " ... ", removed)
    return removed


def filter_lyrics(playlist_row, cachedStopWords):
    
    lyrics = playlist_row['lyrics'][0]
    
    if lyrics.startswith("Couldn't get lyrics for"):
        return ['']
   
    # replace characters/words that are not a part of the lyrics with a space
    lyrics = remove(lyrics)
    
    # remove stopwords
    lyrics = ' '.join([word for word in lyrics.lower().split() if word not in cachedStopWords])
    lyrics = lyrics.split(" ... ")
    
    # frequency of each word
    count_transformer = CountVectorizer()
    lyrics_count = count_transformer.fit_transform(lyrics)
    
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(lyrics_count)
    tf_idf = tfidf_transformer.transform(lyrics_count)
    
    words = count_transformer.get_feature_names()
    tfifd_df = pd.DataFrame(tf_idf[1].T.todense(), index=words, columns=["tf-idf"])
    tfifd_df = tfifd_df.sort_values(by=["tf-idf"], ascending=False)
    return tfifd_df.to_json(orient = 'index')


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
    
    # nltk.download('stopwords')
    cachedStopWords = stopwords.words("english")
    songs_df['lyrics_tfidf'] = songs_df.apply(lambda row : filter_lyrics(row, cachedStopWords), axis=1)
    songs_df.to_csv("playlist_lyrics.csv")
    
    print("Done")


if __name__ == '__main__':
    playlist_csv = sys.argv[1]
    main(playlist_csv)