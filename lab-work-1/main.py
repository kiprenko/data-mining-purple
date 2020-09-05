import csv
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

FILE_NAME = 'sms-spam-corpus.csv'
MESSAGE_TYPE = 'v1'
MESSAGE = 'v2'
SPAM = 'spam'
HAM = 'ham'
spam_dict = {}
ham_dict = {}


def read_csv_file(csv_file):
    return csv.DictReader(csv_file, delimiter=',')


if __name__ == '__main__':
    data = []
    with open(FILE_NAME) as file:
        csv_data = read_csv_file(file)
        for line in csv_data:
            data.append(line)
        file.close()

    for line in data:
        message_ = line[MESSAGE]
        message_ = re.sub('\d+', ' ', message_)
        message_ = re.sub(r'[^a-zA-Z0-9]+', ' ', message_)
        message_ = message_.lower()
        stop_words = set(stopwords.words('english'))
        stop_words.update(['lt', 'gt'])
        word_tokens = word_tokenize(message_)
        filtered_sentence = []

        for word in word_tokens:
            if word not in stop_words and len(word) > 1:
                word = PorterStemmer().stem(word)
                if line[MESSAGE_TYPE] == SPAM:
                    if word in spam_dict:
                        spam_dict[word] += 1
                    else:
                        spam_dict[word] = 1
                else:
                    if word in ham_dict:
                        ham_dict[word] += 1
                    else:
                        ham_dict[word] = 1

    print('Spam dictionary length: ' + str(len(spam_dict)))
    print('Ham dictionary length: ' + str(len(ham_dict)))

    with open('spam-words.json', 'w') as file:
        file.write(json.dumps(sorted(spam_dict.items(), key=lambda x: x[1], reverse=True)))

    with open('ham-words.json', 'w') as file:
        file.write(json.dumps(sorted(ham_dict.items(), key=lambda x: x[1], reverse=True)))

