import libtorrent as lt
from datetime import datetime
import time
import asyncio
import sys


class Client:
    def __init__(self):
        self.session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
        self.active_torrents = []
        self.status = self.session.status()

    async def Add(self, uri, savePath):
        params = {
            'save_path': savePath,
            'storage_mode': lt.storage_mode_t(2),
        }
        try:
            handle = lt.add_magnet_uri(self.session, uri, params)
            self.active_torrents.append(handle)
        except Exception as e:
            print(e)

    def Manage(self):
        if self.active_torrents.__len__() > 0:
            h = self.active_torrents[-1]
            status = h.status()
            _cur_time = time.strftime("%H:%M:%S", time.localtime())
            _progress = format((status.progress * 100), ".2f")
            _download_rate = format((status.download_rate / 1000), ".1f")
            _upload_rate = format((status.upload_rate / 1000), ".1f")
            _peers = status.num_peers
            _name = h.name()[0:30]
            _response = "{}    Progress {}    Download {} kB/s     Upload {} kB/s     {} Peers    {}".format(_name, _progress, _download_rate, _upload_rate, _peers, _cur_time)
            return _response
        else:
            return "No Active Torrents At This Time"
