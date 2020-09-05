import json
import matplotlib.pyplot as plt
import numpy as np

SPAM_BAR_TITLE = 'Top 20 spam words'
HAM_BAR_TITLE = 'Top 20 ham words'
SPAM_WORDS_FILE_NAME = 'spam-words.json'
HAM_WORDS_FILE_NAME = 'ham-words.json'


def show_top_20_words(file_name, title='No name'):
    with open(file_name) as file:
        spam_words = json.load(file)
    frequent_spam_words_stat = spam_words[0:20]
    frequent_spam_words = [word[0] for word in frequent_spam_words_stat]
    frequent_spam_counts = [word[1] for word in frequent_spam_words_stat]
    ypos = np.arange(len(frequent_spam_words))
    plt.yticks(ypos, frequent_spam_words)
    plt.barh(ypos, frequent_spam_counts)
    plt.xlabel('words')
    plt.ylabel('count')
    plt.title(title)

    plt.show()


if __name__ == '__main__':
    show_top_20_words(SPAM_WORDS_FILE_NAME, SPAM_BAR_TITLE)
    show_top_20_words(HAM_WORDS_FILE_NAME, HAM_BAR_TITLE)
