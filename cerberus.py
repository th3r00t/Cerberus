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

import asyncio
import argparse
import locale
import time
import curses
from lib.Torrent import Client
from lib.Display import Display
from lib.Config import Config
from lib.Search import Search

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
state = 0
keypress = None
config = Config()
magnets = []
run = True
Cerberus = {
    'Config': config,
    'TorrentManager': Client(config.storagemaps),
    'Display': Display(),
    'Search': Search(config.endpoints)
}
Cerberus["Config"].getconfig()

logo = """
                            : .:: ^ ~~!7777??????????777!!~^: . .:   :
                          . ^J~ .J?~^!!~^^::............::^~~!!^!J! .77 .
                        ::^.^!7^~J~??^                       :!J!7J.7~? ^::.
                    .~7J?~^.!.:^77: 7!?~.      ..::.       :!77~ ~J^~ !^.~7J?!^.
                 :!?J7^..^.!: :^?^  ~!.J? .^!^^~?YY7~:~~: ^5!.?. .!!^. ~::^ :~?J?~.
                .5J:      !~ .^:J: ^77 .77...:^!JYY?~:...^?^ ^?7. 7!^:  ?:     .~5?
                .5J     :^J::^!.~! JJ!. .?7?777JYYYY?77??7!  ^7Y~.?.^!^:~?:     :57
                 J5. .:!7~?7JJ7::!7YJ!^.  .7~~755Y55J!~!~   :^?YJ!~.~?JJ!7~7^.  ~P~
                 ~?:^:~J?JYYY7^ ~7JY?!^.::^!JYYY5Y55YYY?!^:::~7JY77:.~JYYY?Y7^^:~J.
                .^~^.^?YJ55J7~~~YY5J~!^YP5555JJJYYYJJJY5555P7~~7YY57^~!?Y5YJY!::~~:
              .7^...^7!7?!~^::^???Y~:P5Y?7?7!!!?7JJ?7!~7?7?J5P?.?Y7Y~^::^~7?!!!:..:~!
             .!^^!7?5J?YJ7~.  ^7^JJ~YYJ?~^^...!!!??!!^ .:^^!JY5?!Y7~7.  :!?YY75J77~:!~
             ^J~YJJ57^PY?~~:  7!~5J?!?PY5YJ!^.:!!77!~ :^?JYY55!7JYJ^?^ .^~!J5Y^Y5?JJ~J
             ~5J~7?J?JY?!~:  ~7:!YY? 7B5YYPG5J~^777!^7YPP5YYGP.:YYY.!7:  ^~7JY??J?~7YJ:
           :^^~JYJJ????~~~~^::7^7J7Y^.~YJ7!J55Y7JJY??5557!7Y?^.7J!J^!!::^~~~!????JYJ7^^^.
        .::^!JY55P55J?77!!!!:~?~~Y^~J!:7B7~^^~?YJYYJY!^:~^PG:^7J:7Y:?7:^!!!77??Y5P555Y?~^::.
     .~~::!YPP5YJY5Y?!~^^^!!:.J7^Y?~?5J~?JJ~:^~~?YY!~^::??J!!Y5!!5?^J7.~!~^^~~7J5YYYYPG5?^:^~^.
  :77.^!J5Y?!~~!!77~:..~^?7~..?? 757~7GPYJ!^^^:!JYYJ~:^^~?JYG5~~J5.~J! :!?!~:..:~!!!~~~7J5Y?~:^J~.
 .7!J755Y7~^~^~~^:. .^77!!~:.::7~^~??^!555YJ7!^!JYY?^~!?Y55PY^!J~~:7~::.^~7!7!:. .:^^~^^^!?55Y7?!!
   .7?~!??!!~:   :.~7JJ!^::^.:.!?!. 7Y77555G5Y7^7YY~~?YPGY5J7?Y~ ^7J::::^::~?Y?!::.  .~~!7?7~!J^.
     .:!^?P^ :::7?JYY?7~: :Y7  ^:??~~~^!~^^?Y7~~?YJ7~!JY!^^!~~^!!J!:: .J7 .^!7JYJJ7!.^  ?P~~~..
          :: :J7?77?J!.    ^Y?.  .:77!7~  :!557!JYY7!JP?~. :!7!?~.   ^Y?.    :?J77???7  :.
              :^:~7!:       .JY^    .~??~ ?J5GY?7??7J5GYY^ 7?7..    75!        ^!!^:^.
                              !57.    .J?.?Y57~!777!!^5YY^^J!     :YY:
                               :JY^    :7?^~7J77~~~!7?J!^!?~:   .75!
                                 ~Y?:   :7!.~7!~:..^!7!::?!    ~YJ:
                                  .7Y7.   ~7^~^~777!^^~~7:   ^JY~
                                    :?Y7.  .^!~^~!~^^7~:.  ^JY!
                                      :?Y7.   ^^~7!^^:   ^JY!.
                                        :7Y7:          ~JJ~.
                                          .!YJ~     .!JJ^
                                             ~?J7:^?Y7:
                                               :!J?~.

"""


def header_text():
    return Text("=== Welcome To Cerberus ===",
                justify="center",
                style="bold magenta")


async def keybinds():
    global state, run
    key = Cerberus['Display'].stdscr.getch()
    if key != -1:
        if key == ord('q'):
            Cerberus['Display'].kill()
            run = False
        elif key == ord('/'):
            search = await Cerberus['Display'].search_prompt(Cerberus['Config'], Cerberus['TorrentManager'])
            await asyncio.sleep(.2)
    return False

async def application_loop():
    global state
    Cerberus['Display'].mkheader(),
    Cerberus['Display'].mkfooter()
    while run:
        if state == 0:
            Cerberus['Display'].mkheader(),
            Cerberus['Display'].mkbody(Cerberus['TorrentManager'].Manage()),
            Cerberus['Display'].mkfooter()
            Cerberus['Display'].stdscr.refresh()
            await keybinds()
            await asyncio.sleep(.2)
        if state == 1:
            Cerberus['Display'].mkheader(),
            Cerberus['Display'].mkbody(Cerberus['TorrentManager'].Manage()),
            Cerberus['Display'].mkfooter()
            Cerberus['Display'].stdscr.refresh()
            await keybinds()
            await asyncio.sleep(.2)
        if state == 2:
            Cerberus['Display'].mkheader(),
            Cerberus['Display'].mkbody(Cerberus['TorrentManager'].Manage()),
            Cerberus['Display'].mkfooter()
            Cerberus['Display'].stdscr.refresh()
            await keybinds()
            await asyncio.sleep(.2)
    return "Finished"


async def main():
    """Enter The Realm Of Cerberus."""
    global Cerberus

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config")
    parser.add_argument("-s", "--search")
    args = parser.parse_args()

    if args.config:
        print(f"Config {args.config}.")
    elif args.search:
        _response = Cerberus['Search'].search(args.search)
        for _r in _response:
            print(_r.text)
    else:
        await application_loop()
        await asyncio.sleep(.2)
    print()
    return False


if __name__ == "__main__":
    asyncio.run(main())
    # Cerberus['Display'].kill()
