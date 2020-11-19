import urllib.request as req

import validators
from bs4 import BeautifulSoup

URL_TO_PARSE = 'http://thedemosite.co.uk/'
VISITED_PAGES = []


def main():
    parse_site(req, 'http://thedemosite.co.uk/')


def parse_site(_req, url):
    VISITED_PAGES.append(url)
    req_res = _req.urlopen(url)
    soup = BeautifulSoup(req_res.read(), 'lxml')
    for tag in soup.find_all('a'):
        href_ = tag.attrs["href"]
        if not href_.startswith('http') and not href_.startswith('javascript'):
            print(href_)
            url_to_page = URL_TO_PARSE + href_
            if url_to_page not in VISITED_PAGES and validators.url(url_to_page):
                parse_site(_req, url_to_page)


if __name__ == '__main__':
    main()
