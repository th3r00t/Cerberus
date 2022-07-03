import requests
from bs4 import BeautifulSoup

# https://thepiratebay10.org/search/west%20wing/1/99/0

class Search:

    def __init__(self, config):
        self.endpoints = config
        self.response = None
        self.query = None

    def search(self, query=None, type=1):
        self.query = query
        self.query = self.query.strip()
        self.response = self.get_response(type)
        return self.response

    def make_query(self):
        pass

    def get_response(self, type):
        type = int(type)
        _response = []
        if type == 1:
            ep_type_requested = "tv"
        elif type == 2:
            ep_type_requested = "mv"
        else:
            ep_type_requested = "mv"
        for ep in self.endpoints:
            ep_type = ep[-2:]
            if ep_type == ep_type_requested:
                _str_split = self.endpoints[ep].split('{}')
                _query = _str_split[0] + self.query + _str_split[1]
                _response.append(requests.get(_query))
            else:
                continue
        return self.parse_results(_response)

    def parse_results(self, results):
        parse_out = []
        for result in results:
            soup = BeautifulSoup(result.content, 'html.parser')
            searchResults = soup.find(id='searchResult')
            # srBody = searchResults.find('tbody')
            rows = searchResults.find_all('tr')
            for row in rows[1:-1]:
                try:
                    cols = row.find_all('td')
                    name = cols[1].find('div', class_='detName')
                    name = name.text.strip()
                    magnet = cols[1].find_all('a')
                    magnet = magnet[1].attrs['href']
                    desc = cols[1].find('font', class_='detDesc')
                    desc = desc.text
                    parse_out.append([name, magnet, desc])
                except Exception:
                    pass
        return parse_out
