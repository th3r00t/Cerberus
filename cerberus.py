import asyncio
import argparse
import locale
import time
from rich.live import Live
from rich.console import Text
from rich.panel import Panel
from lib.Torrent import Client
from lib.Display import Display
from lib.Input import Input
from lib.Config import Config
from lib.Search import Search

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
state = None
keypress = None
config = Config()
Cerberus = {
    'Config': config,
    'KeyBindings': Input().kb,
    'TorrentManager': Client(),
    'Display': Display(),
    'Search': Search(config.endpoints)
}
Cerberus["Config"].getconfig()

test_uri = 'magnet:?xt=urn:btih:3271A48DEF3084C93B11A840C55F85CADF160C63&dn\
    =Billy.The.Kid.2022.S01.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV&tr\
    =udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F\
    %2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2F\
    tracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.leechers\
    -paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org\
    %3A6969%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2F\
    announce&tr=udp%3A%2F%2F47.ip-51-68-199.eu%3A6969%2Fannounce&tr=\
    udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=\
    udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2F\
    tracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2F\
    tracker.cyberia.is%3A6969%2Fannounce'

logo = Text("""
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

""",
            style="bold red")


def header_text():
    return Text("=== Welcome To Cerberus ===",
                justify="center",
                style="bold magenta")


def application_loop():
    global state
    while state is None:
        manager = Cerberus['TorrentManager']
        Cerberus['Display'].header.update(Panel(header_text()))
        Cerberus['Display'].body.update(Panel(logo))
        Cerberus['Display'].footer.update(Panel("/ To Begin A Search"))
        with Live(Cerberus['Display']._master_layout(),
                  refresh_per_second=4) as live:
            time.sleep(10)
            for _ in range(20):
                Cerberus['Display'].body.update(Panel(manager.Manage()))
                live.update(Cerberus['Display'].master_layout)
                time.sleep(.4)
        state = True
    return "Finished"


def main():
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
            breakpoint()
            print(_r.text)
    else:
        application_loop()
    print()
    return False


if __name__ == "__main__":
    main()
    # Cerberus['Display'].kill()
