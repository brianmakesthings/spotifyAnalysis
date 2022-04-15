import pandas as pd
import sys

def get_mood():
    
    df = pd.read_csv('Ratings_Warriner_et_al.csv', index_col=0)
    df = df[['Word','V.Mean.Sum', 'A.Mean.Sum','D.Mean.Sum']]
  
    df.columns=['word', 'valence', 'arousal', 'dominance']
    df.set_index('word',inplace=True)
    words = df.to_dict('index')
    return df, words

def get_valence_arousal_dominance(row):
    
    mood_df, words = get_mood()
    lyric = row['lyrics_filtered']
    
    if lyric == 'Error: No lyrics found':
        row['valence_lyrics'] = None
        row['arousal_lyrics'] = None 
        row['dominance_lyrics'] = None
        return row
    
    lyric = lyric.split(' ')
    
    # remove duplicate words
    lyric = list(dict.fromkeys(lyric))
    word_count = len(lyric)
    
    valence_sum = 0
    arousal_sum = 0
    dominance_sum = 0
    
    for word in lyric:
        if word in words:
            valence_sum += words[word]['valence']
            arousal_sum += words[word]['arousal']
            dominance_sum += words[word]['dominance']

    valence = valence_sum / word_count
    arousal = arousal_sum / word_count
    dominance = dominance_sum / word_count
    
    row['valence_lyrics'] = valence
    row['arousal_lyrics'] = arousal
    row['dominance_lyrics'] = dominance
    
    return row



def main(playlist_csv):
    lyrics_df = pd.read_csv(playlist_csv)
    lyrics_df = lyrics_df.apply(get_valence_arousal_dominance, axis=1)
    lyrics_df.to_csv(playlist_csv, index = False)


if __name__ == '__main__':
    playlist_csv = sys.argv[1]
    main(playlist_csv)