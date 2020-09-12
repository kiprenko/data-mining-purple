import csv
import re
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
STOP_WORDS_FILE_NAME = 'stop_words.txt'
MSG_TYPE_KEY = 'v1'
MSG_KEY = 'v2'

SPEC_SYMBOLS_RGX = 'amp;|gt;|lt;|[=!,*)@#%(&$_?.^:;/\\\\"\'\\-]'
NUMBERS_RGX = '[0-9]'
STOP_WORDS = get_stopwords()
ps = PorterStemmer()

if __name__ == '__main__':
    with open(DATA_FILE_NAME) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            msg = row[MSG_KEY]
            msg = process_str(msg)
            print(msg)
