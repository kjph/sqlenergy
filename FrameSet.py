import Tkinter as tk
from Tkinter import Label, Frame, Listbox, Button

class FrameSet(tk.Frame):
    """
    Window for selecting tables
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        #Pack the regions
        self.top_label = Label(self, text="Settings", font="Arial 9 bold")
        self.top_label.pack(anchor=tk.W)

        #Core frame under title (split vertically)
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=tk.X)

        #Frame for containing buttons
        self.btn_frame = Frame(self.main_frame)
        self.btn_frame.pack(side=tk.LEFT)

        self.btn_load_list = Button(self.btn_frame, text="Load", width=8)
        self.btn_load_list.pack()

        self.btn_fetch_list = Button(self.btn_frame, text="Fetch", width=8)
        self.btn_fetch_list.pack()

        self.btn_sel_all = Button(self.btn_frame, text="All", width=8)
        self.btn_sel_all.pack()

        self.btn_sel_all = Button(self.btn_frame, text="Solar", width=8)
        self.btn_sel_all.pack()
