import os
import Tkinter as tk
from Tkinter import Label, Frame
from FrameConnect import FrameConnect
from FrameTable import FrameTable
from FrameQuery import FrameQuery
import collections

class Context():

    def __init__(self):
        self.dbi = {'host': None, 'user': None, 'passwd': None, 'db': None, 'port': 3306}
        self.tab_stat = collections.defaultdict(dict)
        self.last_conn = 0
        self.output_file = None
        self.dir_opt = {'initialdir':os.path.expanduser('~')}

    def add_table(self, table, **stat):
        if ('stype' not in stat or 'thr_min' not in stat or
            'thr_max' not in stat or 'time_format' not in stat) and len(stat) != 4:

            logging.warning("CTX:ERR:Attempted to add table in bad format")
        else:
            self.tab_stat[table] = stat
            logging.debug("CTX:add_table:%s:%s" % (table,stat))

    def del_table(self, table):
        self.tab_stat[table] = {}
        self.tab_stat.pop(table, None)
        logging.debug("CTX:del_table:%s" % table)

class WindowMain(tk.Frame):
    """
    Primary container
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        #Title
        self.parent = parent
        self.parent.title("CSIRO Energy Analyzer")

        #Context container to pass to children
        self.ctx = Context()
        self.ctx.status = tk.StringVar(value="Ready.")
        self.ctx.global_config = {'padx': 5, 'pady': 5}
        self.ctx.const = {'win_width': 760}

        #Master Frame to contain main widgets
        self.main = Frame(self.parent)
        self.main.pack()

        #Status bar
        self.status_label = Label(self.parent, textvariable=self.ctx.status, font="Default 8")
        self.status_label.pack(anchor=tk.W)

        self.create_ui()

    def create_ui(self):
        #UI Layout
        self.main_connect_label = Label(self.main, text="test")

        self.main_connect = FrameConnect(self.main, self.ctx, bd=2, relief=tk.GROOVE)
        self.main_connect.pack(fill=tk.BOTH)

        self.main_table = FrameTable(self.main, self.ctx, bd=2, relief=tk.GROOVE)
        self.main_table.pack(fill=tk.BOTH)

        self.main_query = FrameQuery(self.main, self.ctx, bd=3, relief=tk.GROOVE)
        self.main_query.pack(fill=tk.BOTH)

if __name__ == '__main__':
    root = tk.Tk()
    WindowMain(root)
    root.mainloop()
