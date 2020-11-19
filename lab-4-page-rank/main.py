import urllib.request as req
from pprint import pprint

import validators
from bs4 import BeautifulSoup

HOST = 'http://thedemosite.co.uk/'
VISITED_PAGES = []
PAGES_GRAPH = {}


def main():
    print(f'Started parsing of host {HOST}')
    parse_site()


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


if __name__ == '__main__':
    main()
    pprint(PAGES_GRAPH)
