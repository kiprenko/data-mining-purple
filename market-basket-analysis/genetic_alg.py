import json
import sys
import time
from random import randint
from random import seed

import pandas as pd

seed(1)
INPUT_FILE_NAME = sys.argv[1]
PERCENT = 0.05
K = 3
GENERATIONS_COUNT = 100
TOURNAMENTS_COUNT = 20
MUTATION_NUMBER = 77


def get_purchases(df):
    purchases = []
    for customer_id in df.CustomerID.unique():
        customers_purchases = []
        for stock_code in df[df.CustomerID == customer_id].StockCode:
            customers_purchases.append(str(stock_code))
        purchases.append(customers_purchases)
    return purchases


def get_products(df):
    return [str(product) for product in list(df.StockCode.unique())]


def population_formation(purchases, n_pop):
    chromosomes = []
    rand_nums = []
    purchases_len = len(purchases)
    for i in range(n_pop):
        while True:
            rand_num = randint(0, purchases_len - 1)
            purchase = purchases[rand_num]
            if rand_num not in rand_nums and len(purchase) >= K:
                rand_nums.append(rand_num)
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
    fitness_ = 0
    for i in range(len(purchases)):
        if all(chromosome[j] in purchases[i] for j in range(K)):
            fitness_ += 1
    return fitness_


def genetic_algorithm(chromosomes, purchases, products):
    for i in range(GENERATIONS_COUNT):
        for j in range(TOURNAMENTS_COUNT):
            tournament(chromosomes, purchases)
        mutation(chromosomes, products, purchases)
    return chromosomes


def tournament(chromosomes, purchases):
    parents = selection(chromosomes)
    crossbreeding(parents, purchases, chromosomes)


def selection(chromosomes):
    parents = []
    rand_nums = []
    chromosomes_len = len(chromosomes)
    for i in range(2):
        chromosome_1 = get_rand_chromosome(chromosomes, chromosomes_len, rand_nums)
        chromosome_2 = get_rand_chromosome(chromosomes, chromosomes_len, rand_nums)
        if chromosome_1[K] > chromosome_2[K]:
            parents.append(chromosome_1)
        else:
            parents.append(chromosome_2)
    return parents


def get_rand_chromosome(chromosomes, chromosomes_len, rand_nums):
    while True:
        rand_num = randint(0, chromosomes_len - 1)
        if rand_num not in rand_nums:
            rand_chromosome = chromosomes[rand_num].copy()
            rand_chromosome.append(rand_num)
            return rand_chromosome


def crossbreeding(parents, purchases, chromosomes):
    parent_1 = parents[0]
    parent_2 = parents[1]
    pos_1 = parent_1[K + 1]
    pos_2 = parent_2[K + 1]
    del parent_1[K + 1]
    del parent_2[K + 1]
    child_1 = parent_1.copy()
    child_2 = parent_2.copy()
    crosses = 0
    for i in range(K):
        if crosses == K - 1:
            break
        parent_1_gene = parent_1[i]
        parent_2_gene = parent_2[i]
        if parent_1_gene not in parent_2 and parent_2_gene not in parent_1:
            child_1[i] = parent_2_gene
            child_2[i] = parent_1_gene
            crosses += 1
    child_1[K] = fitness(purchases, child_1)
    child_2[K] = fitness(purchases, child_2)
    if parent_1[K] < child_1[K] and is_chromosome_unique(child_1, chromosomes):
        chromosomes[pos_1] = child_1
    if parent_2[K] < child_2[K] and is_chromosome_unique(child_2, chromosomes):
        chromosomes[pos_2] = child_2


def is_chromosome_unique(chromosome, chromosomes):
    for i in range(len(chromosomes)):
        if all(chromosome[j] in chromosomes[i] for j in range(K)):
            return False
    return True


def mutation(chromosomes, products, purchases):
    for i in range(len(chromosomes)):
        if MUTATION_NUMBER == randint(1, 100):
            mutated_chromosome = chromosomes[i].copy()
            gene_pos = randint(0, K - 1)
            new_gene = products[randint(0, len(products))]
            mutated_chromosome[gene_pos] = new_gene
            if is_chromosome_unique(mutated_chromosome, chromosomes):
                mutated_chromosome[K] = fitness(purchases, mutated_chromosome)
                chromosomes[i] = mutated_chromosome


def main():
    df = pd.read_excel(INPUT_FILE_NAME)
    purchases = get_purchases(df)
    products = get_products(df)
    n_pop = int(len(purchases) * PERCENT)
    chromosomes = population_formation(purchases, n_pop)
    chromosomes = genetic_algorithm(chromosomes, purchases, products)
    chromosomes.sort(reverse=True, key=lambda c: c[K])
    print('Final population\n', json.dumps(chromosomes[:10], indent=4))


if __name__ == '__main__':
    start = time.time()
    main()
    print('Time spent: ', time.time() - start)
