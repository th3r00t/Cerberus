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
        breakpoint()
        if int(savePath) == 1:
            savePath = self.storage_maps['tv']
        elif int(savePath) == 2:
            savePath = self.storage_maps['mv']
        params = {
            'save_path': savePath,
            'storage_mode': lt.storage_mode_t(2),
        }
        try:
            handle = lt.add_magnet_uri(self.session, uri, params)
            asyncio.sleep(.2)
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
