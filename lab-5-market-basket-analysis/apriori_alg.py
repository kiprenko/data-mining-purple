import json
from collections import Counter

import pandas as pd

INPUT_FILE_NAME = 'Filtered Online Retail.xlsx'
SUPPORT = 1000


def get_buckets(df):
    buckets_ = {}
    for customer_id in df.CustomerID.unique():
        # nan check
        if customer_id == customer_id:
            buckets_[int(customer_id)] = list(df[df.CustomerID == customer_id].StockCode)
    return buckets_


def get_one_elem_candidates(df):
    goods = dict(Counter(df['StockCode']))
    return [g for g, c in goods.items() if c > SUPPORT]


def get_two_elem_candidates(one_elem_candidates, buckets):
    two_elem_candidates = []
    one_elem_candidates_len = len(one_elem_candidates)
    for i in range(0, one_elem_candidates_len):
        for j in range(i + 1, one_elem_candidates_len - 1):
            candidates_i_ = one_elem_candidates[i]
            two_elem_candidates.append([candidates_i_, one_elem_candidates[j]])
    two_elem_candidates_counter = Counter()
    for bucket in buckets.values():
        for candidate_pair in two_elem_candidates:
            if candidate_pair[0] in bucket and candidate_pair[1] in bucket:
                pair_key = str(candidate_pair)
                if pair_key in two_elem_candidates_counter:
                    two_elem_candidates_counter[pair_key] += 1
                else:
                    two_elem_candidates_counter[pair_key] = 1
    return dict(two_elem_candidates_counter)


def main():
    df = pd.read_excel(INPUT_FILE_NAME)
    buckets = get_buckets(df)
    print('BUCKETS:\n', json.dumps(buckets, indent=4))
    one_elem_candidates = get_one_elem_candidates(df)
    print('ONE ELEMENT CANDIDATES LENGTH IS', len(one_elem_candidates))
    # print('ONE ELEMENT CANDIDATES:\n', json.dumps(one_elem_candidates, indent=4))
    two_elem_candidates = get_two_elem_candidates(one_elem_candidates, buckets)
    print('TWO ELEMENTS CANDIDATES LENGTH IS', len(two_elem_candidates))
    # print('TWO ELEMENTS CANDIDATES:\n', json.dumps(two_elem_candidates, indent=4))


if __name__ == '__main__':
    main()
