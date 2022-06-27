from rich.table import Table
from rich.table import Column
from rich.layout import Layout

class Display:

    def __init__(self):
        self.header = Layout(name="header", size=3)
        self.body = Layout(name="body")
        self.footer = Layout(name="footer", size=3)
        self.master_layout = Layout()

    def _master_layout(self):
        self.master_layout.split_column(self.header, self.body, self.footer)
        return self.master_layout
