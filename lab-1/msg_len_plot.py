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
    for item in d.items():
        c = item[1]
        x += item[0] * c
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
        spam_w_dict = {word[0]: word[1] for word in Counter(spam_w_list).most_common()}
        ham_w_dict = {word[0]: word[1] for word in Counter(ham_w_list).most_common()}
        spam_w_count = sum(spam_w_dict.values())
        ham_w_count = sum(ham_w_dict.values())
        spam_w_dict = {word[0]: word[1] / spam_w_count for word in spam_w_dict.items()}
        ham_w_dict = {word[0]: word[1] / ham_w_count for word in ham_w_dict.items()}
        draw_chart(spam_w_dict, SPAM)
        draw_chart(ham_w_dict, HAM)


def draw_chart(dict, msg_type):
    plt.style.use('fivethirtyeight')
    plt.title('{} message length chart'.format(msg_type))
    count_of_words = [c for c in dict.keys()]
    x_indexes = np.arange(len(count_of_words))
    plt.xticks(x_indexes, count_of_words)
    plt.bar(x_indexes, [c for c in dict.values()], color='#006a71', label='count of msg by length')
    plt.xlabel("message length")
    plt.ylabel("count of messages")
    plt.show()
    print('Average {} message count = {}'.format(msg_type, str(calculate_avg(dict))))


# Вивести на графіках розподіл по довжині повідомлень для кожної категорії і середню довжину повідомлення.
if __name__ == '__main__':
    main()
