import csv
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class TrainingDataProcessor:
    WORD_KEY = 'word'
    COUNT_KEY = 'count'
    spam_file_name = ''
    ham_file_name = ''
    SPEC_SYMBOLS_RGX = 'amp;|gt;|lt;|[=!,*)@#%(&$_?.^:;/\\\\"\'\\-]'
    NUMBERS_RGX = '[0-9]'
    STOP_WORDS_FILE_NAME = 'stop_words.txt'
    ps = PorterStemmer()

    def __init__(self, spam_file_name, ham_file_name):
        self.spam_file_name = spam_file_name
        self.ham_file_name = ham_file_name

    def print_file_names(self):
        print(f'Spam file name is "{self.spam_file_name}"\nHam file name is "{self.ham_file_name}"')

    def classify_message(self, message):
        print('Preparing message...')
        original_message = message
        message = self.prepare_message(message)
        print(f'Prepared message: "{message}"\nLoading training data from files to memory...')
        spam_word_count = self.__load_training_data(self.spam_file_name)
        ham_word_count = self.__load_training_data(self.ham_file_name)
        print('Training data was successfully loaded\nCalculating probability for both spam and ham...')
        spam_probability = self.calc_probability(spam_word_count, message)
        ham_probability = self.calc_probability(ham_word_count, message)
        if spam_probability == -1 and ham_probability == -1:
            print("The words in the message are unknown for both dictionaries, so it should be HAM.")
            return

        print(f'Spam probability is "{spam_probability}"\nHam probability is "{ham_probability}"\n'
              f'Making normalization...')
        probabilities_sum = spam_probability + ham_probability
        spam_probability_normalized = spam_probability / probabilities_sum
        ham_probability_normalized = ham_probability / probabilities_sum
        print(f'Normalized:\n'
              f'Spam probability is "{spam_probability_normalized}"\nHam probability is "{ham_probability_normalized}"'
              f'\nClassifying the message...')
        if spam_probability_normalized > ham_probability_normalized:
            print(f'The message "{original_message}" is a SPAM')
        else:
            print(f'The message "{original_message}" is a HAM')

    def __load_training_data(self, file_name):
        word_count = {}
        with open(file_name) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                word_count[row[self.WORD_KEY]] = row[self.COUNT_KEY]
        return word_count

    def calc_probability(self, word_count_dict, message):
        total_words_count = self.get_total_words_count(word_count_dict)
        unknown_words_count = self.get_unknown_words_count(message, word_count_dict)
        if unknown_words_count == len(message):
            return -1
        percent = 1
        for word in message:
            w_count = 0
            if word in word_count_dict:
                w_count = int(word_count_dict[word])
            percent *= (w_count + 1) / (total_words_count + unknown_words_count)
        return percent

    def get_total_words_count(self, word_count_dict):
        total_words_count = 0
        for word in word_count_dict:
            total_words_count += int(word_count_dict[word])
        return total_words_count

    def get_unknown_words_count(self, message, word_count_dict):
        unknown_words_count = 0
        known_words = word_count_dict.keys()
        for word in message:
            if word not in known_words:
                unknown_words_count += 1
        return unknown_words_count

    def prepare_message(self, message):
        message = self.rm_spec_symbols(message)
        message = self.rm_numbers(message)
        message = message.lower()
        message = self.rm_stopwords(message)
        return self.stem(message)

    def get_stopwords(self):
        stop_words = set(stopwords.words('english'))
        with open(self.STOP_WORDS_FILE_NAME) as my_sw_file:
            my_sw = re.sub('\n', ' ', my_sw_file.read())
            stop_words.update(word_tokenize(my_sw))
        return stop_words

    def rm_spec_symbols(self, string):
        return re.sub(self.SPEC_SYMBOLS_RGX, ' ', string)

    def rm_numbers(self, string):
        return re.sub(self.NUMBERS_RGX, '', string)

    def rm_stopwords(self, string):
        word_tokens = word_tokenize(string)
        filtered_string = ''
        for w in word_tokens:
            if w not in self.get_stopwords() and len(w) > 2:
                filtered_string = filtered_string + ' ' + w
        return filtered_string.lstrip()

    def stem(self, string):
        tokenized_message = word_tokenize(string)
        stemmed_tokenized_message = []
        for w in tokenized_message:
            stemmed_tokenized_message.append(self.ps.stem(w))
        return stemmed_tokenized_message
