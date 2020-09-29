class TrainingDataProcessor:
    spam_file_name = ''
    ham_file_name = ''

    def __init__(self, spam_file_name, ham_file_name):
        self.spam_file_name = spam_file_name
        self.ham_file_name = ham_file_name

    def print_file_names(self):
        print(f"Spam file name '{self.spam_file_name}'\nHam file name '{self.ham_file_name}'")
