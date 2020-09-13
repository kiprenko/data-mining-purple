from matplotlib import pyplot as plt
import csv


SPAM_FILE = 'output/spam_words.csv'
HAM_FILE = 'output/ham_words.csv'
WORD = 'word'
COUNT = 'count'


def main():
    with open(SPAM_FILE) as f:
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
    plt.title('word length chart')
    plt.tight_layout()
    slices = w_len_dict.values()
    labels = w_len_dict.keys()
    plt.pie(slices, labels=labels)
    plt.show()


# Вивести на графіках розподіл по довжині слів для кожної категорії і середню довжину слів.
if __name__ == '__main__':
    main()
