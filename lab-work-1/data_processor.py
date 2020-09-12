import csv
import re

file_name = 'sms-spam-corpus.csv'
MSG_TYPE_KEY = 'v1'
MSG_KEY = 'v2'


def process_str(string):
    string = rm_spec_symbols(string)
    string = rm_numbers(string)
    string = string.lower()
    return string


def rm_spec_symbols(string):
    rg = 'amp;|gt;|lt;|[\\-!,*)@#%(&$_?.^:;/\\\\"]'
    return re.sub(rg, '', string)


def rm_numbers(string):
    rg = '[0-9]'
    return re.sub(rg, '', string)


if __name__ == '__main__':
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            msg = row[MSG_KEY]
            msg = process_str(msg)
            print(msg)
