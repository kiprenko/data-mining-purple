import json
import time
from random import randint
from random import seed

import pandas as pd

seed(1)
# INPUT_FILE_NAME = 'Filtered Online Retail.xlsx'
INPUT_FILE_NAME = 'test.XLSX'
PERCENT = 0.05
K = 3


def get_buckets(df):
    buckets_ = []
    for customer_id in df.CustomerID.unique():
        buckets_.append(list(df[df.CustomerID == customer_id].StockCode))
    return buckets_


def population_formation(buckets, n_pop):
    chromosomes = []
    random_numbers = set()
    buckets_len = len(buckets)
    for i in range(n_pop):
        while True:
            rand_num = randint(0, buckets_len - 1)
            bucket = buckets[rand_num]
            if rand_num not in random_numbers and len(bucket) >= K:
                random_numbers.add(rand_num)
                break
        chromosomes.append(generate_chromosome(bucket))
    return chromosomes


def generate_chromosome(bucket):
    chromosome = []
    bucket_len = len(bucket)
    for i in range(K):
        while True:
            rand_num = randint(0, bucket_len - 1)
            gene = str(bucket[rand_num])
            if gene not in chromosome:
                chromosome.append(gene)
                break
    return chromosome


def main():
    df = pd.read_excel(INPUT_FILE_NAME)
    buckets = get_buckets(df)
    n_pop = int(len(buckets) * PERCENT)
    chromosomes = population_formation(buckets, n_pop)
    print(json.dumps(chromosomes, indent=4))


if __name__ == '__main__':
    start = time.time()
    main()
    print('Time spent: ', time.time() - start)
