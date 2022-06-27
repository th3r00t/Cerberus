import asyncio
import requests

# https://thepiratebay10.org/search/west%20wing/1/99/0

class Search:

    def __init__(self, config):
        self.endpoints = config

    def search(self, query=None):
        response = self.get_response(query)
        return response

    def make_query(self):
        pass

    def get_response(self, query):
        _response = []
        for ep in self.endpoints:
            _str_split = self.endpoints[ep].split('{}')
            _query = _str_split[0] + query + _str_split[1]
            _response.append(requests.get(_query))
        return _response
