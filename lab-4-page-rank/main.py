import json
import sys
import urllib.request as req

import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup

HOST = sys.argv[1]
VISITED_PAGES = []
WHITE_LIST = ['php', 'html', 'htm', 'jsp', 'asp']
PAGE_DATA = {}


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
    soup = BeautifulSoup(req_res.read(), 'html.parser')
    links = soup.find_all('a')
    for link in links:
        url_to_another_page = link.attrs['href']
        if not url_to_another_page == '#' and not url_to_another_page.startswith(
                'http') and not url_to_another_page.startswith('javascript') \
                and url_to_another_page.split(".")[-1] in WHITE_LIST:
            PAGE_DATA[url].append(url_to_another_page)
            if url_to_another_page not in VISITED_PAGES:
                parse_site(url_to_another_page)


def draw_graph():
    page_graph = nx.DiGraph(pairs_list())
    pos = nx.spring_layout(page_graph)
    nx.draw_networkx(page_graph, pos, with_labels=True)
    plt.title(f'Graph of pages at {HOST}')
    plt.show()
    return page_graph


def pairs_list():
    list_ = []
    for page in PAGE_DATA.items():
        for target_page in page[1]:
            list_.append((page[0], target_page))
    return list_


def main():
    print(f'Started parsing of host {HOST}')
    collect_graph_data()
    graph = draw_graph()
    print(json.dumps(nx.pagerank(graph), indent=4))


if __name__ == '__main__':
    main()
