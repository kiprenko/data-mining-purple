import json
import time
from random import randint
from random import seed

import pandas as pd

seed(1)
INPUT_FILE_NAME = 'Filtered Online Retail.xlsx'
# INPUT_FILE_NAME = 'test.XLSX'
PERCENT = 0.05
K = 3


def get_purchases(df):
    purchases = []
    for customer_id in df.CustomerID.unique():
        purchases.append(list(df[df.CustomerID == customer_id].StockCode))
    return purchases


def population_formation(purchases, n_pop):
    chromosomes = []
    random_numbers = set()
    purchases_len = len(purchases)
    for i in range(n_pop):
        while True:
            rand_num = randint(0, purchases_len - 1)
            purchase = purchases[rand_num]
            if rand_num not in random_numbers and len(purchase) >= K:
                random_numbers.add(rand_num)
                break
        chromosome = generate_chromosome(purchase)
        chromosome.append(fitness(purchases, chromosome))
        chromosomes.append(chromosome)
    return chromosomes


def generate_chromosome(purchase):
    chromosome = []
    purchase_len = len(purchase)
    for i in range(K):
        while True:
            rand_num = randint(0, purchase_len - 1)
            gene = str(purchase[rand_num])
            if gene not in chromosome:
                chromosome.append(gene)
                break
    return chromosome


def fitness(purchases, chromosome):
    fitness = 0
    for i in range(len(purchases)):
        if all(gene in str(purchases[i]) for gene in chromosome):
            fitness += 1
    return fitness


def main():
    df = pd.read_excel(INPUT_FILE_NAME)
    purchases = get_purchases(df)
    n_pop = int(len(purchases) * PERCENT)
    chromosomes = population_formation(purchases, n_pop)
    print(json.dumps(chromosomes, indent=4))


if __name__ == '__main__':
    start = time.time()
    main()
    print('Time spent: ', time.time() - start)
