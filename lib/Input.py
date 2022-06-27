import curses
from prompt_toolkit.key_binding import KeyBindings

class Input:
    def __init__(self):
        self.kb = KeyBindings()
        self.keybinds()

    def keybinds(self):
        @self.kb.add('c-q')
        def _exit(event):
            event.app.exit()
        @self.kb.add('c-s')
        def search(event):
            print("Search")
