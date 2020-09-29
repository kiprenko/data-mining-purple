import csv
import re
from collections import Counter
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def get_stopwords():
    stop_words = set(stopwords.words('english'))
    with open(STOP_WORDS_FILE_NAME) as my_sw_file:
        my_sw = re.sub('\n', ' ', my_sw_file.read())
        stop_words.update(word_tokenize(my_sw))
    return stop_words


def process_str(string):
    string = rm_spec_symbols(string)
    string = rm_numbers(string)
    string = string.lower()
    string = rm_stopwords(string)
    return string


def rm_spec_symbols(string):
    return re.sub(SPEC_SYMBOLS_RGX, ' ', string)


def rm_numbers(string):
    return re.sub(NUMBERS_RGX, '', string)


def rm_stopwords(string):
    word_tokens = word_tokenize(string)
    filtered_string = ''
    for w in word_tokens:
        if w not in STOP_WORDS and len(w) > 2:
            filtered_string = filtered_string + ' ' + w
    return filtered_string.lstrip()


def stem(string):
    word_tokens = word_tokenize(string)
    stem_string = ''
    for w in word_tokens:
        stem_string = stem_string + ' ' + ps.stem(w)
    return stem_string.lstrip()


DATA_FILE_NAME = 'sms-spam-corpus.csv'
OUTPUT_DIR = 'output'
SPAM_OUTPUT_FILE = 'spam_words_count.csv'
HAM_OUTPUT_FILE = 'ham_words_count.csv'
STOP_WORDS_FILE_NAME = 'stop_words.txt'
MSG_TYPE_KEY = 'v1'
MSG_KEY = 'v2'
SPAM = 'spam'
HAM = 'ham'

SPEC_SYMBOLS_RGX = 'amp;|gt;|lt;|[=!,*)@#%(&$_?.^:;/\\\\"\'\\-]'
NUMBERS_RGX = '[0-9]'
STOP_WORDS = get_stopwords()
ps = PorterStemmer()


def write_to_file(list, f_name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(OUTPUT_DIR + '/' + f_name, 'w', newline='') as f:
        fieldnames = ['word', 'count']
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        for key, value in list:
            csv_writer.writerow({'word': key, 'count': value})


def main():
    with open(DATA_FILE_NAME) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        spam_w_counter = Counter()
        ham_w_counter = Counter()
        for row in csv_reader:
            tokenized_msg = word_tokenize(process_str(row[MSG_KEY]))
            if row[MSG_TYPE_KEY] == SPAM:
                spam_w_counter.update(tokenized_msg)
            else:
                ham_w_counter.update(tokenized_msg)

        write_to_file(spam_w_counter.most_common(), SPAM_OUTPUT_FILE)
        write_to_file(ham_w_counter.most_common(), HAM_OUTPUT_FILE)


if __name__ == '__main__':
    main()
