# Import packages
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
import sys

def main(playlist):
    df = pd.read_csv(playlist)

    words = ""

    output = []

    for lyric in df['lyrics']:
        for word in lyric.split(' '):
            if (word.lower().isalpha()):
                words += word+" "
            else:
                if "," in word:
                    word = word.replace(",", "")
                    if word.find("\n"):
                        temp_words = word.lower().split("\\n")
                        for temp_word in temp_words:
                            temp_word = temp_word.replace("\\n", "")
                            if (temp_word.lower().isalpha()):
                                temp_word = temp_word.replace("\\", "")
                                words += temp_word+" "
                            elif "'" in temp_word:
                                temp_word = temp_word.replace("\\", "")
                                words += temp_word+" " 
                            elif "," in temp_word:
                                more_temp_words = word.lower().split(',')
                                for more_temp_word in more_temp_words:
                                        words += more_temp_word+" "
                    else:
                        words += word+" "
                elif word.find("\\n"):
                        temp_words = word.lower().split("\\n")
                        for temp_word in temp_words:
                            temp_word = temp_word.replace("\\n", "")
                            if (temp_word.lower().isalpha()):
                                temp_word = temp_word.replace("\\", "")
                                words += temp_word+" "
                            elif "'" in temp_word:
                                temp_word = temp_word.replace("\\", "")
                                words += temp_word+" " 
                            elif "," in temp_word:
                                more_temp_words = word.lower().split(',')
                                for more_temp_word in more_temp_words:
                                    if (temp_word.lower().isalpha()):
                                        more_temp_word = more_temp_word.replace("\\", "")
                                        words += more_temp_word+" "
                elif "'" in word:
                    words += word+" " 

    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', colormap='Set2', collocations=False, stopwords = STOPWORDS).generate(words)

    wordcloud.to_file("wordcloud.png")

if __name__ == '__main__':
    main(sys.argv[1])




