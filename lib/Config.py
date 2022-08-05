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

import configparser
from pathlib import Path


class Config:
    def __init__(self):
        self.endpoints = {}
        self.tvdbkey = ""
        self.moviedbkey = ""
        self.storagemaps = {}
        if not Path('./cerberus.ini').is_file():
            self.mkconfig()
        else:
            self.getconfig()

    @staticmethod
    def mkconfig():
        #
        _file = configparser.ConfigParser()
        _file["Endpoints"] = {
            "tpbmv": "https://thepiratebay.rocks/search/{}/1/99/201",  # Movies
            "tpbtv": "https://thepiratebay.rocks/search/{}/1/99/205",  # Tv
            "tpbgm": "https://thepiratebay.rocks/search/{}/1/99/400",  # Games
            "tpbms": "https://thepiratebay.rocks/search/{}/1/99/100",  # Music
            "tpbab": "https://thepiratebay.rocks/search/{}/1/99/102",  # ABooks
            "tpbeb": "https://thepiratebay.rocks/search/{}/1/99/601",  # EBooks
            "tpbcm": "https://thepiratebay.rocks/search/{}/1/99/602",  # Comics
            "tpbca": "https://thepiratebay.rocks/search/{}/1/99/0",  # CatchAll
        }
        _file["Storage"] = {
            "tv": "./tv",
            "mv": "./mov",
            "gm": "./games",
            "ms": "./music",
            "ab": "./abook",
            "eb": "./ebook",
            "cm": "./comic",
            "ca": "./other"
        }
        with open(r"cerberus.ini", 'w') as configObj:
            _file.write(configObj)
            configObj.flush()
            configObj.close()

    def getconfig(self):
        _file = configparser.ConfigParser()
        _file.read('./cerberus.ini')
        for endpoint in _file["Endpoints"]:
            self.endpoints[endpoint] = _file["Endpoints"][endpoint]
        for _path in _file["Storage"]:
            self.storagemaps[_path] = _file["Storage"][_path]
