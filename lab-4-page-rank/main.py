import json
import math
import operator
import urllib.request as req
from itertools import islice

import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup

HOST = 'http://thedemosite.co.uk/'
PLOT_STYLE = 'fivethirtyeight'
VISITED_PAGES = []
PAGE_DATA = {}
D = 0.50


def collect_graph_data():
    parse_site()
    print(json.dumps(PAGE_DATA, indent=4))


def parse_site(url='/'):
    VISITED_PAGES.append(url)
    PAGE_DATA[url] = []
    try:
        request = req.Request(HOST + url, headers={'User-Agent': 'Mozilla/5.0'})
        req_res = req.urlopen(request)
    except:
        return
    soup = BeautifulSoup(req_res.read(), 'lxml')
    links = soup.find_all('a')
    for link in links:
        url_to_another_page = link.attrs['href']
        if not url_to_another_page == '#' and not url_to_another_page.startswith(
                'http') and not url_to_another_page.startswith('javascript'):
            PAGE_DATA[url].append(url_to_another_page)
            if url_to_another_page not in VISITED_PAGES:
                parse_site(url_to_another_page)


def draw_graph():
    page_graph = nx.DiGraph(pairs_list())
    pos = nx.spring_layout(page_graph)
    nx.draw_networkx(page_graph, pos, with_labels=False)
    plt.title(f'Graph of pages at {HOST}')
    plt.style.use(PLOT_STYLE)
    plt.show()
    return page_graph


def pairs_list():
    list_ = []
    for page in PAGE_DATA.items():
        for target_page in page[1]:
            list_.append((page[0], target_page))
    return list_


def find_id(graph, node):
    index = 0
    for nd in graph.nodes:
        if node == nd:
            return index
        index += 1


def jacobi_method(matrix_b):
    e = 0.01
    solve_vector = []
    new_vector = []
    for i in range(0, len(matrix_b)):
        solve_vector.append(matrix_b[i][len(matrix_b)])
    eps = 1
    while eps > e:
        for i in range(0, len(matrix_b)):
            sum_ = 0
            for j in range(0, len(solve_vector)):
                sum_ += + solve_vector[i] * matrix_b[i][j]
            sum_ += + matrix_b[i][len(matrix_b)]
            new_vector.append(sum_)
        eps = 0
        for i in range(0, len(solve_vector)):
            eps = eps + math.fabs(new_vector[i] - solve_vector[i])

        solve_vector = new_vector.copy()
        new_vector.clear()
    final_dict = dict()
    for i in range(0, len(solve_vector)):
        final_dict[i] = solve_vector[i]
    final_dict = sorted(final_dict.items(), key=operator.itemgetter(1), reverse=True)
    return final_dict


def main():
    print(f'Started parsing of host {HOST}')
    collect_graph_data()
    graph = draw_graph()
    matrix_b = [[0 for x in range(len(graph.nodes) + 1)] for y in range(len(graph.nodes))]
    print(json.dumps(matrix_b, indent=4))

    dict_count_link = {}
    for key, value in PAGE_DATA.items():
        dict_count_link[key] = len(value)
    for i in graph.edges:
        matrix_b[find_id(graph, i[1])][find_id(graph, i[0])] = D / dict_count_link[i[0]]

    print(json.dumps(matrix_b, indent=4))
    for i in range(0, len(matrix_b)):
        matrix_b[i][len(matrix_b)] = 1 - D

    solution = jacobi_method(matrix_b)
    for key, value in list(islice(solution, 10)):
        print(value)


if __name__ == '__main__':
    main()
