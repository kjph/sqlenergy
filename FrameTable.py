import Tkinter as tk
from Tkinter import Label, Frame, Listbox, Button, Entry
import hquery

class FrameTable(tk.Frame):
    """
    Window for selecting tables
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.ctx = ctx

        #Pack the regions
        self.top_label = Label(self, text="Select Tables", font="Arial 9 bold")
        self.top_label.pack(anchor=tk.W)

        #Core frame under title (split vertically)
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=tk.X)

        self.fetched_listbox = Listbox(self.main_frame, width=40)
        self.fetched_listbox.pack(side=tk.LEFT)

        #Build the select options (buttons between two listboxes)
        self.select_frame = Frame(self.main_frame)
        self.select_frame.pack(side=tk.LEFT)
        self.initUI_select_frame(self.select_frame)

        self.table_listbox = Listbox(self.main_frame, width=40)
        self.table_listbox.pack(side=tk.LEFT)

        #Frame for containing buttons
        self.btn_frame = Frame(self)
        self.btn_frame.pack()
        self.initUI_btn_frame(self.btn_frame)

    def initUI_select_frame(self, parent):

        self.select_btn_del = Button(parent, text="<< Remove", width=10)
        self.select_btn_del.pack()

        self.select_btn_add = Button(parent, text="Add as >>", width=10)
        self.select_btn_add.pack()

        self.select_type = Entry(parent, width=10)
        self.select_type.pack()

    def initUI_btn_frame(self, parent):
        self.btn_load_list = Button(self.btn_frame, text="Load", width=8)#, command=self.load_tables)
        self.btn_load_list.pack(side=tk.LEFT)

        self.btn_fetch_list = Button(self.btn_frame, text="Fetch", width=8, command=self.fetch_tables)
        self.btn_fetch_list.pack(side=tk.LEFT)

        self.btn_sel_all = Button(self.btn_frame, text="All", width=8)
        self.btn_sel_all.pack(side=tk.LEFT)

    def fetch_tables(self):

        if self.ctx.last_conn:
            self.fetched_listbox.delete(0, tk.END)
            all_tables = hquery.get_all_tables(**self.ctx.dbi)
            for tab, col in enumerate(sorted(all_tables)):
                self.fetched_listbox.insert(tab,col)

            self.fetched_listbox.update_idletasks()
        else:
            self.ctx.status.set("Please test connection first")

    #def load_tables(self):
