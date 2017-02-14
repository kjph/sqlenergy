import os
import logging
import sys
from collections import OrderedDict
import Tkinter as tk
from Tkinter import Label, Button, Entry, Listbox, Frame, Canvas
import tkFileDialog as filedialog
from sqlenergy import core
import ViewModel
from ttk import *

class FrameConnect(tk.Frame):
    """
    Window for connecting to database
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.ctx = ctx
        ViewModel.set_update_func(ctx, staticmethod(self.update_context))
        ViewModel.add_func_group(ctx, staticmethod(self.clear_context), 'clearAll')

        #'Global' string variables
        self.strvars = {}

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(self, [('info', {'fill': tk.BOTH, 'side':tk.LEFT}),
                                       ('file', {'fill': tk.BOTH, 'side':tk.RIGHT})])

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
                       {'fill': tk.X})

        parent.widgets = {'top':        Label(parent.frames['top'], text="OR Load Configuration",
                                              font=self.ctx.const['font_title']),
                          'label':      Label(parent.frames['main'], text="File:"),
                          'entry':      Entry(parent.frames['main'], textvariable=self.strvars['dbi_file'],
                                              width=self.ctx.const['win_width']/20),
                          'btn_find':   Button(parent.frames['main'], text="...",
                                               command=self.get_dbi_file_dialog, width=3),
                          'btn_load':   Button(parent.frames['core'], text="Load",
                                               command=self.get_dbi_file_user_input, width=7),
                          'btn_conn':   Button(parent.frames['core'], text="Ping",
                                               command=self.ping_database, width=7),
                          'btn_clear':  Button(parent.frames['core'], text="Clear",
                                               command=self.clear_context, width = 7)}

        packing = [('top',   {'anchor': tk.W, 'side': tk.LEFT}),
                   ('label', {'fill': tk.X, 'side': tk.LEFT, 'extconf': self.ctx.global_widget_conf}),
                   ('entry', {'fill': tk.X, 'side': tk.LEFT, 'extconf': self.ctx.global_widget_conf}),
                   ('btn_load', {'side': tk.RIGHT, 'extconf': self.ctx.global_widget_conf}),
                   ('btn_find', {'side': tk.RIGHT, 'extconf': self.ctx.global_widget_conf}),
                   ('btn_conn', {'side': tk.RIGHT, 'extconf': self.ctx.global_widget_conf}),
                   ('btn_clear', {'side': tk.RIGHT, 'extconf': self.ctx.global_widget_conf})]
        ViewModel.pack_widgets(parent.widgets, packing)


    def initUI_info(self, parent):

        # TODO
        # Re-factor this code to be more explicit

        # BUG
        # 'passwd' entry does not fit

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

    def update_context(self, clear=False):
        """
        Output to Context
        """

        for var in self.ctx.dbi_fields:
            val = self.frames['info'].widgets[var].get().strip()
            if val != '':
                self.ctx.dbi[var] = val
            elif var in self.ctx.dbi_defaults:
                self.ctx.dbi[var] = self.ctx.dbi_defaults[var]
            elif not(clear):
                self.ctx.status.set("Please insert value for %s" % var)
                return 0
        return 1

    def get_dbi_file_dialog(self):
        """
        To find file with explorer
        """

        target = filedialog.askopenfile()

        if not(target):
            return 0
        else:
            self.ctx.dbi_file = target.name
            self.strvars['dbi_file'].set(self.ctx.dbi_file)
            r = self.load_dbi_file()
            return r

    def get_dbi_file_user_input(self):
        """
        For loading file from user entered string
        """

        wid = ViewModel.get_widget(self, 'file', 'entry')
        target = wid.get()

        if not(os.path.isfile(target)):
            self.ctx.status.set("ERR: File not found")
            return 0
        else:
            self.ctx.dbi_file = target
            self.load_dbi_file()

        return 1

    def load_dbi_file(self):
        """
        Get settings from file
        """

        if self.ctx.dbi_file == None:
            self.ctx.status.set("Please enter the path to your config file")
            return 0

        dbi = core.fetchInputs.database_inputs(self.ctx.dbi_file)

        #If file could not be read
        if dbi == -1:
            self.ctx.status.set("ERR: File format not supported")
            return 0

        for var in self.ctx.dbi_fields:

            #If missing fields
            if var not in dbi:
                self.ctx.status.set("ERR: Incomplete config")
                return 0

            #Set the values
            self.strvars[var].set(dbi[var])
            self.frames['info'].widgets[var].configure(state='readonly')

        logging.debug("FrameConnect:%s" % self.ctx.dbi)

        if self.update_context():
            self.ctx.status.set("Ready.")
        else:
            return 0

        self.ctx.on_call('databaseLoad')
        return 1

    def ping_database(self):
        """
        Attempt to connect to server
        """

        self.ctx.status.set("Pinging...")
        if not(self.update_context()):
            return 0

        if core.hquery.ping_database(**self.ctx.dbi):
            self.ctx.status.set("Success")
            self.ctx.on_call('databaseLoad')
            return 1
        else:
            self.ctx.status.set("Failed to Connect")
            return 0

    def clear_context(self):
        """
        Clear all information in entry widgets and clear context
        """

        for var in self.ctx.dbi:
            self.frames['info'].widgets[var].configure(state='normal')
            self.strvars[var].set("")

        self.ctx.dbi_file = None
        self.strvars['dbi_file'].set("")

        self.update_context(True)#Clear mode
        self.ctx.status.set("Cleared. Ready.")

        return 1
