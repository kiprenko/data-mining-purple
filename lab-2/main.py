from TrainingDataProcessor import TrainingDataProcessor

if __name__ == '__main__':
    print('Welcome to Saint-Tropez')
    data_processor = TrainingDataProcessor('spam_words_count.csv', 'ham_words_count.csv')
    data_processor.print_file_names()
    data_processor.classify_message(input('Type your message: '))
