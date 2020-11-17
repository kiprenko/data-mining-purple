import matplotlib.pyplot as plt
import pandas as pd

DATA_SET_FILE_NAME = 'points_datasets/s1.txt'


def load_dataset(file_name):
    return pd.read_csv(file_name, header=None, delim_whitespace=True)


if __name__ == '__main__':
    data_set = load_dataset(DATA_SET_FILE_NAME)
    plt.plot(data_set, 'go')
    plt.show()
