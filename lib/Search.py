# Cerberus, Torrent Aggregator
# Copyright (C) 2022 th3r00t

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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
        elif type == 3:
            ep_type_requested = "gm"
        elif type == 4:
            ep_type_requested = "ms"
        elif type == 5:
            ep_type_requested = "ab"
        elif type == 6:
            ep_type_requested = "eb"
        elif type == 7:
            ep_type_requested = "cm"
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
