import pandas as pd
import regex as re
import string
import math
import sys

def number_of_occurences(word, lyric):
    # The translate table takes in characters to remove and characters to keep
    # as both arguments.
    return lyric.lower().split().count(word)

# Count how many times word occured in all the lyrics
def num_lyrics_containing_word(word, lyrics):
    count = 0
    for lyric in lyrics:
        if (number_of_occurences(word.lower(), lyric) > 0):
            count += 1
    return count

def main(playlist):
    df = pd.read_csv(playlist)
    # Accounting for the number of times a word occurs in a lyric
    word_occurence = 0
    Total_TFIDF_Score = []
    word_set = set()
    word_list = []
    total_number_of_lyrics = len(df['lyrics_filtered'])
    res = 0

    for lyric in df['lyrics_filtered']:
        lyric_length = len(lyric) - lyric.count(' ')
        for word in lyric.split():
            if (word.lower().isalpha() and (word.lower() not in word_set)):
                if word.lower() != "tyrics":
                    word_occurence += number_of_occurences(word.lower(), lyric)
                    TF_Score = word_occurence / lyric_length
                    IDF_Score = math.log(total_number_of_lyrics / num_lyrics_containing_word(word, df['lyrics_filtered']))
                    TFIDF_Score = TF_Score * IDF_Score
                    Total_TFIDF_Score.append(TFIDF_Score)
                    word_list.append(word)
                    word_set.add(word.lower())

    lyrics_df = pd.DataFrame({'Words': word_list, 'TFIDF_Score_Per_Word': Total_TFIDF_Score})
    lyrics_df = lyrics_df.sort_values('TFIDF_Score_Per_Word', ascending=False)
    lyrics_df.drop_duplicates(subset="Words", keep=False, inplace=True)
    lyrics_df.to_csv("Lyrics_TFIDF_Score", index=False)

if __name__ == '__main__':
    main(sys.argv[1])