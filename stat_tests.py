import sys
import statistics
import math
import pandas as pd
from scipy import stats
import statsmodels.api as sm

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
    word_set = set()
    avg_lyrics_tfidf_scores = []
    total_number_of_lyrics = len(df['lyrics_filtered'])

    for lyric in df['lyrics_filtered']:
        lyric_length = len(lyric) - lyric.count(' ')
        temp_tfidf_scores = []
        for word in lyric.split():
            if (word.lower().isalpha() and (word.lower() not in word_set)):
                if word.lower() != "lyrics":
                    word_occurence += number_of_occurences(word.lower(), lyric)
                    TF_Score = word_occurence / lyric_length
                    IDF_Score = math.log(total_number_of_lyrics / num_lyrics_containing_word(word, df['lyrics_filtered']))
                    TFIDF_Score = TF_Score * IDF_Score
                    temp_tfidf_scores.append(TFIDF_Score)
                    word_set.add(word.lower())
        if (len(temp_tfidf_scores) == 0):
            avg_lyrics_tfidf_scores.append(0)
        else:
            avg_lyrics_tfidf_scores.append(statistics.mean(temp_tfidf_scores))
        

    reg = stats.linregress(avg_lyrics_tfidf_scores, df['popularity'])
    print("The slope of the regression model is: ", reg.slope)
    print("The intercept of the regression model is: ", reg.intercept)
    print("The p-value of the regression model is: ", reg.pvalue)
    print("The regression coefficient is: ", reg.rvalue, "\n")

    results = sm.OLS(avg_lyrics_tfidf_scores, df['popularity']).fit()
    print(results.summary())

if __name__ == '__main__':
    main(sys.argv[1])
