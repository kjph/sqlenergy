import Tkinter as tk
from Tkinter import Label, Frame
from FrameConnect import FrameConnect
from FrameTable import FrameTable
from FrameQuery import FrameQuery

class View(tk.Frame):
    """
    Primary container
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("CSIRO Energy Analyzer")

        #Context container to pass to children
        self.ctx = ctx
        self.ctx.status = tk.StringVar(value="Ready.")
        self.ctx.global_widget_conf = {'padx': 5, 'pady': 2}
        self.ctx.const = {'win_width': 760,#Window width
                          'font_title': "Arial 9 bold"}#Font of titles

        #Master Frame to contain main widgets
        self.main = Frame(self.parent)
        self.main.pack()

        #Status bar
        self.status_label = Label(self.parent, textvariable=self.ctx.status, font="Default 8")
        self.status_label.pack(anchor=tk.W)

        self.initUI()

    def initUI(self):
        #UI Layout
        self.ctx.frames['connect'] = FrameConnect(self.main, self.ctx, bd=2, relief=tk.GROOVE)
        self.ctx.frames['connect'].pack(fill=tk.BOTH)

        self.ctx.frames['table'] = FrameTable(self.main, self.ctx, bd=2, relief=tk.GROOVE)
        self.ctx.frames['table'].pack(fill=tk.BOTH)

        # self.ctx.frames['query'] = FrameQuery(self.main, self.ctx, bd=3, relief=tk.GROOVE)
        # self.ctx.frames['query'].pack(fill=tk.BOTH)
