import os
import logging
import Tkinter as tk
from Tkinter import Label, Frame, Listbox, Button, Entry
import tkFileDialog as filedialog

class FrameQuery(tk.Frame):
    """
    Window for selecting tables
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.ctx = ctx

        #Pack the regions
        self.top_label = Label(self, text="Query", font="Arial 9 bold")
        self.top_label.pack(anchor=tk.W)

        #Core frame under title (split vertically)
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=tk.X)

        #Frame for settings
        self.set_frame = Frame(self.main_frame)
        self.set_frame.pack(fill=tk.X, side=tk.LEFT)
        self.initUI_set_frame(self.set_frame)

        #Frame for containing buttons
        self.btn_frame = Frame(self.main_frame)
        self.btn_frame.pack(fill=tk.X, side=tk.RIGHT)
        self.initUI_btn_frame(self.btn_frame)

    def initUI_set_frame(self, parent):

        #Date settings frame
        self.set_date_frame = Frame(parent)
        self.set_date_frame.pack(fill=tk.X)

        #File settings frame
        self.set_outf_frame = Frame(parent)
        self.set_outf_frame.pack(fill=tk.X)

        #Date: Weidgets
        self.set_date_start_label = Label(self.set_date_frame, text="Start Date:")
        self.set_date_end_label = Label(self.set_date_frame, text="End Date:")

        #Date: Packing
        self.set_date_start_label.pack(side=tk.LEFT)
        self.date_start = {}
        self.initUI_date_entry(self.date_start, self.set_date_frame)
        self.set_date_end_label.pack(side=tk.LEFT)
        self.date_end = {}
        self.initUI_date_entry(self.date_end, self.set_date_frame)

        #File: Dir Widgets
        self.set_outf_dir_label = Label(self.set_outf_frame, text="Output Directory:")
        self.str_set_outf_dir_current = tk.StringVar(value="")
        self.set_outf_dir_current = Entry(self.set_outf_frame, textvariable=self.str_set_outf_dir_current,
                                          state="readonly", width=45)
        self.set_outf_dir_btn = Button(self.set_outf_frame, text="...", command=self.set_output_directory)

        #File: File Widgets
        self.set_outd_file_label = Label(self.set_outf_frame, text="Filename:")
        self.set_outd_file = Entry(self.set_outf_frame, width=30)

        #File: Packing
        self.set_outf_dir_label.pack(side=tk.LEFT)
        self.set_outf_dir_current.pack(side=tk.LEFT)
        self.set_outd_file.pack(side=tk.RIGHT)
        self.set_outd_file_label.pack(side=tk.RIGHT)
        self.set_outf_dir_btn.pack(side=tk.RIGHT)

    def initUI_date_entry(self, container, parent):
        Label(parent, text='Y:').pack(side=tk.LEFT)
        container['Y'] = Entry(parent, width=5)
        container['Y'].pack(side=tk.LEFT)
        Label(parent, text='M:').pack(side=tk.LEFT)
        container['M'] = Entry(parent, width=3)
        container['M'].pack(side=tk.LEFT)
        Label(parent, text='D:').pack(side=tk.LEFT)
        container['D'] = Entry(parent, width=3)
        container['D'].pack(side=tk.LEFT)

    def initUI_btn_frame(self, parent):
        self.btn_fetch_list = Button(parent, text="Clear All", width=8)
        self.btn_fetch_list.pack()

        self.btn_load_list = Button(parent, text="Query", width=8)
        self.btn_load_list.pack()

    def set_output_directory(self):
        """
        To find file with explorer
        """

        user_dir_req = filedialog.askdirectory(title="Select output directory", **self.ctx.dir_opt)
        if not(user_dir_req):
            return

        self.ctx.output_dir = user_dir_req
        self.str_set_outf_dir_current.set(user_dir_req)
        logging.debug("FrameQuery:set_output_directory:%s" % self.ctx.output_dir)

        self.update_context()

    def update_context(self):

        self.ctx.query_start_date = "%s-%s-%s" % (self.date_start['Y'].get().strip(),
                                                  self.date_start['M'].get().strip(),
                                                  self.date_start['D'].get().strip())
        self.ctx.query_start_date = "%s-%s-%s" % (self.date_end['Y'].get().strip(),
                                                  self.date_end['M'].get().strip(),
                                                  self.date_end['D'].get().strip())
