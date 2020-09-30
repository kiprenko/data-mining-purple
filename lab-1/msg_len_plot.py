from collections import Counter
import csv
from matplotlib import pyplot as plt
import numpy as np

DATA_FILE_NAME = 'sms-spam-corpus.csv'
SPAM = 'spam'
HAM = 'ham'
MSG_TYPE_KEY = 'v1'
MSG_KEY = 'v2'


def calculate_avg(d):
    x = 0
    y = 0
    for v in d:
        c = v[1]
        x += v[0] * c
        y += c
    return x / y


def main():
    with open(DATA_FILE_NAME) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        spam_w_list = []
        ham_w_list = []
        for row in csv_reader:
            msg_len = len(row[MSG_KEY])
            if row[MSG_TYPE_KEY] == SPAM:
                spam_w_list.append(msg_len)
            else:
                ham_w_list.append(msg_len)
        spam_w_list = Counter(spam_w_list).most_common()
        ham_w_list = Counter(ham_w_list).most_common()

        draw_chart(spam_w_list, SPAM)
        draw_chart(ham_w_list, HAM)


def draw_chart(cnter, msg_type):
    plt.style.use('fivethirtyeight')
    plt.title('{} message length chart'.format(msg_type))
    count_of_words = [c[0] for c in cnter]
    x_indexes = np.arange(len(count_of_words))
    plt.xticks(x_indexes, count_of_words)
    plt.bar(x_indexes, [c[1] for c in cnter], color='#006a71', label='count of msg by length')
    plt.xlabel("message length")
    plt.ylabel("count of messages")
    plt.show()
    print('Average {} message count = {}'.format(msg_type, str(calculate_avg(cnter))))


# Вивести на графіках розподіл по довжині повідомлень для кожної категорії і середню довжину повідомлення.
if __name__ == '__main__':
    main()
