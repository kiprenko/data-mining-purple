import csv
from matplotlib import pyplot as plt
import numpy as np

SPAM_FILE = 'output/spam_words.csv'
HAM_FILE = 'output/ham_words.csv'
WORD = 'word'
COUNT = 'count'
TITLE = 'Top 20 {} words'
SPAM = 'spam'
HAM = 'ham'


def main():
    draw_chart(SPAM_FILE, SPAM)
    draw_chart(HAM_FILE, HAM)


def draw_chart(f_name, msg_type):
    with open(f_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        words = []
        frequencies = []
        for row in csv_reader:
            words.append(row[WORD])
            frequencies.append(row[COUNT])
        plt.style.use('fivethirtyeight')
        plt.title(TITLE.format(msg_type))
        words = words[0:20]
        words.reverse()
        total_count_of_w = sum([int(frequency) for frequency in frequencies])
        frequencies = [int(frequency) / total_count_of_w for frequency in frequencies[:20]]
        frequencies.reverse()
        x_indexes = np.arange(len(words))
        plt.xticks(x_indexes, words)
        plt.bar(x_indexes, frequencies, color='#006a71', label='Most frequent {} words'.format(msg_type))
        plt.xlabel("words")
        plt.ylabel("frequency")
        plt.gca().invert_xaxis()
        plt.show()


if __name__ == '__main__':
    main()
