import os
import sys
import ntpath
import Tkinter as tk
from Tkinter import Label, Button, Entry, Listbox, Frame, Canvas
import tkFileDialog as filedialog

class FrameConnect(tk.Frame):
    """
    Window for connecting to database
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        #Context
        self.ctx = ctx
        self.global_config = ctx.global_config

        #Pack the regions
        self.top_label = Label(self, text="Specify Database Information", font="Arial 9 bold")
        self.top_label.pack(anchor=tk.W)

        self.top_frame = Frame(self, bd=4)
        self.top_frame.pack(fill=tk.X)

        self.mid_rule=Frame(self,height=1,width=ctx.const['win_width'],bg="gray")
        self.mid_rule.pack()

        self.mid_label = Label(self, text="OR Load Configuration", font="Arial 9 bold")
        self.mid_label.pack(anchor=tk.W)

        self.mid_frame = Frame(self)
        self.mid_frame.pack(fill=tk.X)

        self.bot_frame = Frame(self,bd=5)
        self.bot_frame.pack(fill=tk.X)

        self.status = ctx.status

        self.init_ui_top()
        self.init_ui_mid()


    def init_ui_mid(self):
        """
        For loading configuration files
        """

        m = self.mid_frame

        self.file_current_name = tk.StringVar(value="None")

        self.file_label = Label(m, text="File:")
        self.file_label.pack(side=tk.LEFT, **self.global_config)

        self.file_entry = Entry(m, textvariable=self.file_current_name, width=self.ctx.const['win_width']/8)
        self.file_entry.pack(fill=tk.X, side=tk.LEFT, **self.global_config)

        self.file_button = Button(m, text="Load", command=self.load_file, width=7)
        self.file_button.pack(side=tk.RIGHT, **self.global_config)

        self.file_button = Button(m, text="...", command=self.find_file, width=3)
        self.file_button.pack(side=tk.RIGHT, **self.global_config)

    def init_ui_top(self):
        """
        For manual specification
        """

        m = self.top_frame

        #Specify grid manager
        host_row, host_col = [2, 0]
        cred_row, cred_col = [3, 0]
        db_row, db_col = [4, 0]
        connect_row, connect_col = [4,5]

        #Host
        self.host_label = Label(m, text="Host:")
        self.host_label.grid(row=host_row, column=host_col, sticky='E')

        self.host_current = tk.StringVar(value="")
        self.host_entry = Entry(m, textvariable=self.host_current)
        self.host_entry.grid(row=host_row, column=host_col+1, sticky='W')

        #Cred
        self.user_label = Label(m, text="User:")
        self.user_label.grid(row=cred_row, column=cred_col, sticky='E')

        self.user_current = tk.StringVar(value="")
        self.user_entry = Entry(m, textvariable=self.user_current)
        self.user_entry.grid(row=cred_row, column=cred_col+1, sticky='W')

        self.passwd_label = Label(m, text="Passwd:")
        self.passwd_label.grid(row=cred_row, column=cred_col+2, sticky='E')

        self.passwd_current = tk.StringVar(value="")
        self.passwd_entry = Entry(m, show="*", textvariable=self.passwd_current)
        self.passwd_entry.grid(row=cred_row, column=cred_col+3, sticky='W')

        #db
        self.db_label = Label(m, text="Database:")
        self.db_label.grid(row=db_row, column=db_col, sticky='E')

        self.db_current = tk.StringVar(value="")
        self.db_entry = Entry(m, textvariable=self.db_current)
        self.db_entry.grid(row=db_row, column=db_col+1, sticky='W')

        self.port_label = Label(m, text="Port:")
        self.port_label.grid(row=db_row, column=db_col+2, sticky='E')

        self.port_current = tk.StringVar(value="3306")
        self.port_entry = Entry(m, textvariable=self.port_current)
        self.port_entry.grid(row=db_row, column=db_col+3, sticky='W')

        self.connect_button = Button(m, text="Ping", command=self.connect, width=10)
        self.connect_button.grid(row=connect_row, column=connect_col+1, **self.ctx.global_config)

        self.clear_button = Button(m, text='Clear', command=self.clear_settings, width=8)
        self.clear_button.grid(row=connect_row, column=connect_col, **self.ctx.global_config)


    def find_file(self):
        """
        To find file with explorer
        """

        user_open_req = filedialog.askopenfile()
        if not(user_open_req):
            return

        self.data_file = user_open_req.name
        self.file_current_name.set(self.data_file)

        self.set_settings()

    def load_file(self):
        """
        For loading file from user entered string
        """

        self.data_file = self.file_entry.get()

        if not(os.path.isfile(self.data_file)):
            self.status.set("ERR: File not found")
            return
        else:
            self.set_settings()

    def set_settings(self):
        """
        Get settings from file
        """

        dbi = core.fetchInputs.database_inputs(self.data_file)
        if dbi == -1:
            self.status.set("ERR: File format not supported")
            return
        elif ('host' not in dbi or 'user' not in dbi or
              'passwd' not in dbi or 'db' not in dbi or
              'port' not in dbi):

             self.status.set("ERR: Incomplete config")
             return

        self.host_current.set(dbi['host'])
        self.user_current.set(dbi['user'])
        self.passwd_current.set(dbi['passwd'])
        self.db_current.set(dbi['db'])
        self.port_current.set(dbi['port'])

        self.host_entry.configure(state='readonly')
        self.user_entry.configure(state='readonly')
        self.passwd_entry.configure(state='readonly')
        self.db_entry.configure(state='readonly')
        self.port_entry.configure(state='readonly')

        self.update_context()

        self.status.set("Ready.")

        self.connect()

    def connect(self):
        """
        Attempt to connect to server
        """
        self.status.set("Pinging...")

        self.update_context()

        if core.hquery.ping_database(**self.ctx.dbi):
            self.status.set("Success")
            self.ctx.last_conn = 1
        else:
            self.status.set("Failed to Connect")

    def clear_settings(self):
        """
        Clear all information
        """

        self.host_entry.configure(state='normal')
        self.user_entry.configure(state='normal')
        self.passwd_entry.configure(state='normal')
        self.db_entry.configure(state='normal')
        self.port_entry.configure(state='normal')

        self.status.set("Cleared. Ready.")
        self.host_current.set("")
        self.user_current.set("")
        self.passwd_current.set("")
        self.db_current.set("")
        self.port_current.set("3306")
        self.file_current_name.set("")

        self.ctx.last_conn = 0
        self.update_context()

    def update_context(self):

        self.ctx.dbi['host'] = self.host_entry.get().strip()
        self.ctx.dbi['user'] = self.user_entry.get().strip()
        self.ctx.dbi['passwd'] = self.passwd_entry.get().strip()
        self.ctx.dbi['db'] = self.db_entry.get().strip()
        self.ctx.dbi['port'] = self.port_entry.get().strip()

    def exit(self):
        """
        Close
        """

        sys.exit(0)
