import json
import matplotlib.pyplot as plt
import numpy as np

SPAM_BAR_TITLE = 'Spam words letters count'
HAM_BAR_TITLE = 'Ham words letters count'
SPAM_WORDS_FILE_NAME = 'spam-words.json'
HAM_WORDS_FILE_NAME = 'ham-words.json'


def show_avg_words_len(file_name, title='No name'):
    with open(file_name) as file:
        spam_words = json.load(file)
    len_dict = {}
    for w in spam_words:
        wlen = len(w[0])
        if wlen in len_dict:
            len_dict[wlen] += 1
        else:
            len_dict[wlen] = 1
    ypos = np.arange(len(len_dict))
    plt.yticks(ypos, len_dict.keys())
    plt.barh(ypos, len_dict.values())
    plt.xlabel('count of words')
    plt.ylabel('letters count')
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    show_avg_words_len(HAM_WORDS_FILE_NAME, HAM_BAR_TITLE)
    show_avg_words_len(SPAM_WORDS_FILE_NAME, SPAM_BAR_TITLE)
