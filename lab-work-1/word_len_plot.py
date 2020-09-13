from matplotlib import pyplot as plt
import csv
import numpy as np


SPAM_FILE = 'output/spam_words.csv'
HAM_FILE = 'output/ham_words.csv'
WORD = 'word'
COUNT = 'count'
SPAM_TITLE = 'Count of spam words by length chart'
HAM_TITLE = 'Count of ham words by length chart'


def main(file_name, chart_title):
    with open(file_name) as f:
        csv_reader = csv.DictReader(f)
        w_len_dict = {}
        w_count = 0
        for row in csv_reader:
            w_len = len(row[WORD])
            count_ = int(row[COUNT])
            w_count += count_
            if w_len in w_len_dict:
                w_len_dict[w_len] += count_
            else:
                w_len_dict[w_len] = count_

    plt.style.use('fivethirtyeight')
    plt.title(chart_title)
    words = w_len_dict.keys()
    x_indexes = np.arange(len(words))
    plt.xticks(x_indexes, words)
    plt.bar(x_indexes, w_len_dict.values(), color='#006a71', label='count of words by length')
    plt.xlabel("word length")
    plt.ylabel("count of words")
    plt.show()


# Вивести на графіках розподіл по довжині слів для кожної категорії і середню довжину слів.
if __name__ == '__main__':
    main(SPAM_FILE, SPAM_TITLE)
    main(HAM_FILE, HAM_TITLE)
