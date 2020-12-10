import json
from collections import Counter
import time

import pandas as pd

INPUT_FILE_NAME = 'test.XLSX'
SUPPORT_LEVEL = 2


def get_products(df):
    return [str(product) for product in list(df.StockCode.unique())]


def get_buckets(df):
    buckets_ = {}
    for customer_id in df.CustomerID.unique():
        # nan check
        if customer_id == customer_id:
            buckets_[int(customer_id)] = list(df[df.CustomerID == customer_id].StockCode)
    return buckets_


def filter_one_elem_cand(products, buckets):
    one_elem_candidates = {}
    for customer_id, bucket in buckets.items():
        for product in bucket:
            if product in one_elem_candidates:
                one_elem_candidates[product] += 1
            else:
                one_elem_candidates[product] = 1

    for product, count in one_elem_candidates.items():
        try:
            if count < SUPPORT_LEVEL:
                products.remove(product)
        except ValueError:
            pass
    return products


def get_product_pairs(products):
    product_pairs = []
    products_len = len(products)
    for i in range(products_len - 1):
        for j in range(i + 1, products_len):
            product_pairs.append(tuple([products[i], products[j]]))
    return product_pairs


def filter_two_elem_cand(products, buckets):
    products_pairs = get_product_pairs(products)
    two_elem_candidates = {}
    for bucket in buckets.values():
        for product_pair in products_pairs:
            if product_pair[0] in bucket and product_pair[1] in bucket:
                if product_pair in two_elem_candidates:
                    two_elem_candidates[product_pair] += 1
                else:
                    two_elem_candidates[product_pair] = 1
    products = set()
    for two_elem_candidate, count in Counter(two_elem_candidates).items():
        if count >= SUPPORT_LEVEL:
            products.add(two_elem_candidate[0])
            products.add(two_elem_candidate[1])
    return list(products)


def get_product_triples(products):
    product_triples = []
    products_len = len(products)
    for i in range(products_len - 2):
        for j in range(i + 1, products_len):
            for k in range(j + 1, products_len):
                product_triples.append(tuple([products[i], products[j], products[k]]))
    return product_triples


def filter_three_elem_cand(result, buckets):
    products_triples = get_product_triples(result)
    three_elem_candidates = {}
    for bucket in buckets.values():
        for product_triple in products_triples:
            if product_triple[0] in bucket and product_triple[1] in bucket and product_triple[2]:
                if product_triple in three_elem_candidates:
                    three_elem_candidates[product_triple] += 1
                else:
                    three_elem_candidates[product_triple] = 1
    result = {}
    for candidate_triple, count in three_elem_candidates.items():
        if count >= SUPPORT_LEVEL:
            result[str(candidate_triple)] = count
    return result


def main():
    start = time.time()
    df = pd.read_excel(INPUT_FILE_NAME)
    buckets = get_buckets(df)
    products = get_products(df)
    products = filter_one_elem_cand(products, buckets)
    products = filter_two_elem_cand(products, buckets)
    print(json.dumps(filter_three_elem_cand(products, buckets), indent=4))
    print('Time spent: ', time.time() - start)


if __name__ == '__main__':
    main()
