import urllib.request as req
from pprint import pprint

import validators
from bs4 import BeautifulSoup

URL_TO_PARSE = 'http://thedemosite.co.uk/'
VISITED_PAGES = []
PAGES_GRAPH = {}


def main():
    parse_site(req, 'http://thedemosite.co.uk/')


def parse_site(_req, url):
    VISITED_PAGES.append(url)
    PAGES_GRAPH[url] = []
    req_res = _req.urlopen(url)
    soup = BeautifulSoup(req_res.read(), 'lxml')
    links = soup.find_all('a')
    for link in links:
        href_ = link.attrs['href']
        if not href_.startswith('http') and not href_.startswith('javascript'):
            url_to_page = URL_TO_PARSE + href_
            PAGES_GRAPH[url].append(url_to_page)
            if url_to_page not in VISITED_PAGES and validators.url(url_to_page):
                parse_site(_req, url_to_page)


if __name__ == '__main__':
    main()
    pprint(PAGES_GRAPH)
