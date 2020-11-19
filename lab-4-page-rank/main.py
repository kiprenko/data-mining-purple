import urllib.request as req
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import validators
from bs4 import BeautifulSoup

HOST = 'http://thedemosite.co.uk/'
PLOT_STYLE = 'fivethirtyeight'
VISITED_PAGES = []
PAGES_GRAPH = {}


def main():
    print(f'Started parsing of host {HOST}')
    collect_graph_data()
    draw_graph()


def collect_graph_data():
    parse_site()
    pprint(PAGES_GRAPH)


def parse_site(url='/'):
    VISITED_PAGES.append(url)
    PAGES_GRAPH[url] = []
    req_res = req.urlopen(HOST + url)
    soup = BeautifulSoup(req_res.read(), 'lxml')
    links = soup.find_all('a')
    for link in links:
        url_to_another_page = link.attrs['href']
        if not url_to_another_page.startswith('http') and not url_to_another_page.startswith('javascript'):
            PAGES_GRAPH[url].append(url_to_another_page)
            if url_to_another_page not in VISITED_PAGES and validators.url(HOST + url_to_another_page):
                parse_site(url_to_another_page)


def draw_graph():
    page_graph = nx.MultiDiGraph(pairs_list())
    pos = nx.spring_layout(page_graph)
    nx.draw_networkx(page_graph, pos)
    plt.title(f'Graph of pages at {HOST}')
    plt.style.use(PLOT_STYLE)
    plt.show()


def pairs_list():
    list_ = []
    for page in PAGES_GRAPH.items():
        for target_page in page[1]:
            list_.append((page[0], target_page))
    return list_


if __name__ == '__main__':
    main()
