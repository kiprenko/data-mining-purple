import json
import urllib.request as req

import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup

HOST = 'http://thedemosite.co.uk/'
PLOT_STYLE = 'fivethirtyeight'
VISITED_PAGES = []
PAGE_DATA = {}


def main():
    print(f'Started parsing of host {HOST}')
    collect_graph_data()
    draw_graph()


def collect_graph_data():
    parse_site()
    print(json.dumps(PAGE_DATA, indent=4))


def parse_site(url='/'):
    VISITED_PAGES.append(url)
    PAGE_DATA[url] = []
    try:
        request = req.Request(HOST + url, headers={'User-Agent': 'Mozilla/5.0'})
        page = req.urlopen(request)
    except:
        return
    soup = BeautifulSoup(page.read(), 'lxml')
    links = soup.find_all('a')
    for link in links:
        url_to_another_page = link.attrs['href']
        if not url_to_another_page.startswith('http') and not url_to_another_page.startswith('javascript'):
            PAGE_DATA[url].append(url_to_another_page)
            if url_to_another_page not in VISITED_PAGES:
                parse_site(url_to_another_page)


def draw_graph():
    page_graph = nx.DiGraph(pairs_list())
    pos = nx.spring_layout(page_graph)
    nx.draw_networkx(page_graph, pos)
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


if __name__ == '__main__':
    main()
