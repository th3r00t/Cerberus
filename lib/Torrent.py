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

import libtorrent as lt
import time
import asyncio


class Client:
    def __init__(self, storagemaps):
        self.session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
        self.active_torrents = []
        self.status = self.session.status()
        self.storage_maps = storagemaps

    async def Add(self, uri, savePath):
        if int(savePath) == 1:
            savePath = self.storage_maps['tv']
        elif int(savePath) == 2:
            savePath = self.storage_maps['mv']
        elif int(savePath) == 3:
            savePath = self.storage_maps['gm']
        elif int(savePath) == 4:
            savePath = self.storage_maps['ms']
        elif int(savePath) == 5:
            savePath = self.storage_maps['ab']
        elif int(savePath) == 6:
            savePath = self.storage_maps['eb']
        elif int(savePath) == 7:
            savePath = self.storage_maps['cm']
        else:
            savePath = self.storage_maps['mv']
        params = {
            'save_path': savePath,
            'storage_mode': lt.storage_mode_t(2),
        }
        try:
            handle = lt.add_magnet_uri(self.session, uri, params)
            await asyncio.sleep(.2)
            self.active_torrents.append(handle)
        except Exception as e:
            print(e)

    def Manage(self):
        _response = []
        if self.active_torrents.__len__() > 0:
            for i in self.active_torrents:
                status = i.status()
                _cur_time = time.strftime("%H:%M:%S", time.localtime())
                _progress = format((status.progress * 100), ".2f")
                _download_rate = format((status.download_rate / 1000), ".1f")
                _upload_rate = format((status.upload_rate / 1000), ".1f")
                _peers = status.num_peers
                _name = i.name()
                _response.append([_name, _progress, _download_rate, _upload_rate, _peers])
            # _response = "{}    Progress {}    Download {} kB/s     Upload {} kB/s     {} Peers    {}".format(_name, _progress, _download_rate, _upload_rate, _peers, _cur_time)
            return _response
        else:
            return ["No Active Downloads", "", "", "", ""]
