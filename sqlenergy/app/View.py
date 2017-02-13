import os
import Tkinter as tk
from Tkinter import Label, Frame
import ViewModel
from FrameConnect import FrameConnect
from FrameTable import FrameTable
from FrameSet import FrameSet
from FrameQuery import FrameQuery
from ttk import *

class View(tk.Frame):
    """
    Primary container
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("CSIRO Energy Analyzer")

        #Appearance
        self.parent.Style = Style()
        self.parent.Style.theme_use("xpnative")
        self.parent.Style.configure('.', font=('Helvetica', 9))
        self.parent.Style.map('TButton',
                              background=[('disabled','#d9d9d9'), ('active','#ececec')],
                              foreground=[('disabled','#a3a3a3')],
                              relief=[('pressed', '!disabled', 'sunken')])
        self.parent.Style.configure('TEntry',
                              foreground='#a3a3a3')

        #Context container to pass to children
        self.ctx = ctx
        self.ctx.status = tk.StringVar(value="Ready.")
        self.ctx.global_widget_conf = {'padx': 5, 'pady': 2}
        self.ctx.const = {'win_width': 760,#Window width
                          'font_title': "Arial 9 bold"}#Font of titles
        self.ctx.opts = {'dir': {'initialdir':os.path.expanduser('~')}}

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(parent, ['main', 'status'],
                       **{'fill': tk.BOTH})

        f = ViewModel.get_frame(parent, 'main')
        self.initUI_main(f)

        f = ViewModel.get_frame(parent, 'status')
        self.initUI_status(f)

    def initUI_main(self, parent):
        #UI Layout
        self.frames = {'connect': FrameConnect(parent, self.ctx, bd=2, relief=tk.GROOVE),
                       'table': FrameTable(parent, self.ctx, bd=2, relief=tk.GROOVE),
                       'setting': FrameSet(parent, self.ctx, bd=2, relief=tk.GROOVE),
                       'query': FrameQuery(parent, self.ctx, bd=2, relief=tk.GROOVE)}

        self.frames['connect'].pack(fill=tk.BOTH)
        self.frames['table'].pack(fill=tk.BOTH)
        self.frames['setting'].pack(fill=tk.BOTH)
        self.frames['query'].pack(fill=tk.BOTH)

    def initUI_status(self, parent):
        #Status bar
        self.widgets = {'stat': Label(parent, textvariable=self.ctx.status, font="Default 8")}
        self.widgets['stat'].pack(anchor=tk.W)
