import csv


class TrainingDataProcessor:
    spam_file_name = ''
    ham_file_name = ''

    def __init__(self, spam_file_name, ham_file_name):
        self.spam_file_name = spam_file_name
        self.ham_file_name = ham_file_name

    def print_file_names(self):
        print(f"Spam file name '{self.spam_file_name}'\nHam file name '{self.ham_file_name}'")

    def process_files(self):
        self.__process_file(self.spam_file_name)
        self.__process_file(self.ham_file_name)

    def __process_file(self, file_name):
        total_words_count = 0
        words_popularity = {}
        with open(file_name) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                w_count = row['count']
                total_words_count += int(w_count)
                words_popularity[row['word']] = int(w_count) / total_words_count
        print(words_popularity)
