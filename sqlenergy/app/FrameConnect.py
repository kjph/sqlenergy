import os
import logging
import sys
from collections import OrderedDict
import Tkinter as tk
from Tkinter import Label, Button, Entry, Listbox, Frame, Canvas
import tkFileDialog as filedialog
from . import core
import ViewModel

class FrameConnect(tk.Frame):
    """
    Window for connecting to database
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.ctx = ctx
        ViewModel.set_update_func(ctx, staticmethod(self.update_context))

        #'Global' string variables
        self.strvars = {}

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(self, ['info', 'file'],
                       **{'fill': tk.Y, 'side':tk.LEFT})

        #Create the regions
        self.initUI_info(self.frames['info'])
        self.initUI_file(self.frames['file'])

    def initUI_file(self, parent):
        """
        For loading configuration files
        """

        self.strvars['dbi_file'] = tk.StringVar(value="")

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(parent, ['top', 'main', 'core'],
                       **{'fill': tk.X})

        parent.widgets = {'top': Label(parent.frames['top'], text="OR Load Configuration",
                                            font=self.ctx.const['font_title']),
                          'label': Label(parent.frames['main'], text="File:"),
                          'entry': Entry(parent.frames['main'], textvariable=self.strvars['dbi_file'],
                                         width=self.ctx.const['win_width']/20),
                          'btn_find': Button(parent.frames['main'], text="...",
                                             command=self.get_dbi_file_dialog, width=3),
                          'btn_load': Button(parent.frames['core'], text="Load",
                                             command=self.get_dbi_file_user_input, width=7),
                          'btn_conn': Button(parent.frames['core'], text="Ping",
                                             command=self.ping_database, width=7),
                          'btn_clear': Button(parent.frames['core'], text="Clear",
                                              command=self.clear_context, width = 7)}

        parent.widgets['top'].pack(anchor=tk.W, side=tk.LEFT)
        parent.widgets['label'].pack(fill=tk.X, side=tk.LEFT, **self.ctx.global_widget_conf)
        parent.widgets['entry'].pack(fill=tk.X, side=tk.LEFT, **self.ctx.global_widget_conf)
        parent.widgets['btn_load'].pack(side=tk.RIGHT, **self.ctx.global_widget_conf)
        parent.widgets['btn_find'].pack(side=tk.RIGHT, **self.ctx.global_widget_conf)
        parent.widgets['btn_conn'].pack(side=tk.RIGHT, **self.ctx.global_widget_conf)
        parent.widgets['btn_clear'].pack(side=tk.RIGHT, **self.ctx.global_widget_conf)


    def initUI_info(self, parent):

        parent.widgets = {'top': Label(parent, text="Specify Database Information",
                                             font=self.ctx.const['font_title'])}
        parent.widgets['top'].pack(anchor=tk.W)
        parent.frames = {}

        #Specify which widget (key) should be right of another widget (value)
        adjacent_widgets = {'passwd': 'user',
                            'port': 'db',}

        #Generate Label-Entry pair for each field
        for var in self.ctx.dbi_fields:
            self.strvars[var] = tk.StringVar(value="")
            if var in adjacent_widgets:
                parent.frames[var] = parent.frames[adjacent_widgets[var]]
            else:
                parent.frames[var] = Frame(parent)
                parent.frames[var].pack(fill=tk.X)

            parent.widgets['%s-label' % var] = Label(parent.frames[var], text="%s:" % var.title(), width=6)
            parent.widgets['%s-label' % var].pack(fill=tk.X, side=tk.LEFT, **self.ctx.global_widget_conf)
            parent.widgets[var] = Entry(parent.frames[var], textvariable=self.strvars[var])
            parent.widgets[var].pack(fill=tk.X, side=tk.LEFT, **self.ctx.global_widget_conf)

        parent.widgets['passwd'].configure(show='*')

    def update_context(self):
        """
        Output to Context
        """

        for var in self.ctx.dbi_fields:
            self.ctx.dbi[var] = self.frames['info'].widgets[var].get().strip()

    def get_dbi_file_dialog(self):
        """
        To find file with explorer
        """

        target = filedialog.askopenfile()

        if not(target):
            return
        else:
            self.ctx.dbi_file = target.name
            self.strvars['dbi_file'].set(self.ctx.dbi_file)
            self.load_dbi_file()

    def get_dbi_file_user_input(self):
        """
        For loading file from user entered string
        """

        target = self.file_entry.get()

        if not(os.path.isfile(target)):
            self.ctx.status.set("ERR: File not found")
            return
        else:
            self.ctx.dbi_file = target
            self.load_dbi_file()

    def load_dbi_file(self):
        """
        Get settings from file
        """

        dbi = core.fetchInputs.database_inputs(self.ctx.dbi_file)

        #If file could not be read
        if dbi == -1:
            self.ctx.status.set("ERR: File format not supported")
            return

        for var in self.ctx.dbi_fields:

            #If missing fields
            if var not in dbi:
                self.ctx.status.set("ERR: Incomplete config")
                return

            #Set the values
            self.strvars[var].set(dbi[var])
            self.frames['info'].widgets[var].configure(state='readonly')

        self.update_context()
        logging.debug("FrameConnect:%s" % self.ctx.dbi)

        self.ctx.status.set("Ready.")

    def ping_database(self):
        """
        Attempt to connect to server
        """

        self.ctx.status.set("Pinging...")
        self.update_context()

        if core.hquery.ping_database(**self.ctx.dbi):
            self.ctx.status.set("Success")
            self.ctx.on_call('databaseLoad')
        else:
            self.ctx.status.set("Failed to Connect")

    def clear_context(self):
        """
        Clear all information in entry widgets and clear context
        """

        for var in self.ctx.dbi:
            self.frames['info'].widgets[var].configure(state='normal')
            self.strvars[var].set("")

        self.ctx.dbi_file = None
        self.strvars['dbi_file'].set("")

        self.update_context()
        self.ctx.status.set("Cleared. Ready.")
