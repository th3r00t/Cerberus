import curses
import time
import asyncio
from curses.textpad import Textbox
from curses.textpad import rectangle
from .Search import Search


class Display:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(1)
        self.stdscr.clear()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.rows, self.cols = self.stdscr.getmaxyx()
        self.middle_row = int(self.rows / 2)
        self.middle_col = int(self.cols / 2)
        self.header_msg = "=== Welcome To Cerberus ==="
        self.header = curses.newwin(3, self.cols, 0, 0)
        self.body = curses.newwin(self.rows - 6, self.cols, 3, 0)
        self.footer = curses.newwin(3, self.cols, self.rows - 3, 0)
        self.header.box()
        # self.body.box()
        self.footer.box()

    def mkheader(self):
        self.header.clear()
        self.print_middle_center(self.header_msg, self.header)
        self.print_middle_right("q to quit", self.header)
        self.header.box()
        self.header.refresh()

    def mkbody(self, msg):
        self.body.clear()
        self.body.addstr(0, 0, self.format_body(msg))
        # self.body.box()
        self.body.refresh()

    def mkfooter(self, msg="/ To Search"):
        self.footer.clear()
        self.footer.addstr(1, 2, msg)
        self.footer.box()
        self.footer.refresh()

    def print_middle_center(self, msg, window):
        _window_row, _window_col = window.getmaxyx()
        _ip = int((_window_col / 2) - (len(msg) / 2))
        window.addstr(int(_window_row / 2), _ip, msg)

    def print_middle_right(self, msg, window):
        _window_row, _window_col = window.getmaxyx()
        _ip = int(_window_col - len(msg) - 3)
        window.addstr(int(_window_row / 2), _ip, msg)

    async def search_prompt(self, config, torrent_manager):
        # footer = curses.newwin(3, self.cols, self.rows - 3, 0)
        prompt_window = curses.newwin(1, self.cols-20, self.rows - 2, 14)
        box = Textbox(prompt_window)
        curses.curs_set(1)
        prompt_window.refresh()
        box.edit()
        _search = box.gather()
        self.body.clear()
        # self.body.box()
        self.footer.clear()
        self.mkfooter("Is This 1 a Tv Show, or 2 a Movie? > ")
        prompt_window = curses.newwin(1, self.cols-45, self.rows - 2, 39)
        box = Textbox(prompt_window)
        prompt_window.clear()
        box.edit()
        self.mkbody
        _type = box.gather()
        curses.curs_set(0)
        self.body.refresh()
        await asyncio.sleep(1)
        search_results = Search(config.endpoints).search(_search, _type)
        magnets, scrnout = self.format_body(search_results, 1, True)
        self.body.addstr(scrnout)
        # self.body.box()
        self.body.refresh()
        self.footer.clear()
        self.mkfooter("Select # To Download > ")
        prompt_window.clear()
        box.edit()
        choice = box.gather()
        try:
            choice = int(choice)
            try:
                link = magnets[int(choice)]
                await torrent_manager.Add(link, _type)
                await asyncio.sleep(1)
            except KeyError:
                pass
        except ValueError:
            return False
        return choice

    def format_body(self, results, page=1, search=False):
        _msg_body = ""
        _mY, _mX = self.body.getmaxyx()
        _mY -= 2
        _mX -= 2
        i = 0
        if not search:
            for r in results:
                if i < _mY:
                    try:
                        if len("{} {} {} {} {}".format(r[0], r[1], r[2], r[3], r[4])) < _mX:
                            _msg_body += "\t{}\t{}% complete\tdn: {}kB/s\tup: {}kB/s\t{} peers.\n".format(r[0], r[1], r[2], r[3], r[4])
                        else:
                            overflow = len("{} {} {} {} {}".format(r[0], r[1], r[2], r[3], r[4])) - _mX
                            _msg_body += "\t{}\t{}% complete\tdn: {}kB/s\tup: {}kB/s\t{} peers.\n".format(r[0][0:-overflow], r[1], r[2], r[3], r[4])
                    except IndexError:
                        return "No Active Torrents"
                    i = i = 1
                else:
                    return _msg_body
            return _msg_body
        elif search:
            magnets = []
            i = 0
            for r in results:
                magnets.append(r[1])
                _msg_body += "{}: {} {}\n".format(i, r[0], r[2])
                i += 1
            msg = [magnets, _msg_body]
            return msg

    def kill(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        self.stdscr.nodelay(0)
        curses.endwin()
