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
            "tpbmv": "https://thepiratebay10.org/search/{}/1/99/201",
            "tpbtv": "https://thepiratebay10.org/search/{}/1/99/0"
        }
        _file["Storage"] = {
            "tv": "./tv",
            "mov": "./mov"
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
