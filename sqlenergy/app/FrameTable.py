import logging
from collections import OrderedDict
import Tkinter as tk
import ttk
from Tkinter import Label, Frame, Listbox, Button, Entry
import tkFileDialog as filedialog
from . import core
import ViewModel

class FrameTable(tk.Frame):
    """
    Window for selecting tables
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.ctx = ctx
        ViewModel.add_func_group(ctx, staticmethod(self.fetch_table_from_db), 'databaseLoad')

        self.consts = {'selectTreeCount': 0}

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(self, ['top', 'main', 'btn'],
                       **{'fill': tk.BOTH})

        #Widget
        self.initUI_top(ViewModel.get_frame(self, 'top'))
        self.initUI_main(ViewModel.get_frame(self, 'main'))
        self.initUI_btn(ViewModel.get_frame(self, 'btn'))

    def initUI_top(self, parent):

        parent.widgets = {'top': Label(parent, text="Select Tables", font="Arial 9 bold")}
        parent.widgets['top'].pack(anchor=tk.W)

    def initUI_main(self, parent):

        #Generate the frames for main
        ViewModel.mk_frames_in(parent, ['fetched', 'opts', 'selected'],
                               **{'fill': tk.BOTH, 'side': tk.LEFT})

        #fetched frame
        f = ViewModel.get_frame(parent, 'fetched')
        f.widgets = {'fetchList': Listbox(f, height=15, width=40,
                                          selectmode=tk.EXTENDED)}
        f.widgets['fetchList'].pack()

        #selected frame
        f = ViewModel.get_frame(parent, 'selected')
        self.initUI_main_selected(f)

        #Extended Inits
        f = ViewModel.get_frame(parent, 'opts')
        self.initUI_main_opts(f)

    def initUI_main_opts(self, parent):

        ViewModel.mk_frames_in(parent, self.ctx.stat_fields)
        for var in self.ctx.stat_fields:
            f = ViewModel.get_frame(parent, var)
            f.widgets = {'%s-label' % var: Label(f, text=var),
                         var: Entry(f, width=10)}

            #pack
            f.widgets['%s-label' % var].pack(side=tk.LEFT)
            f.widgets[var] .pack(side=tk.RIGHT)

        btn_size = 12
        parent.widgets = {'btn-add': Button(parent, text=">> Add", width=btn_size, command=self.add_table_selected),
                       'btn-del': Button(parent, text="<< Remove", width=btn_size, command=self.del_table_selected),
                       'btn-reg': Button(parent, text="Regex...", width=btn_size),
                       'btn-all': Button(parent, text="Select All", width=btn_size)}

        parent.widgets['btn-add'].pack()
        parent.widgets['btn-del'].pack(side=tk.BOTTOM)
        parent.widgets['btn-reg'].pack(side=tk.BOTTOM)
        parent.widgets['btn-all'].pack(side=tk.BOTTOM)

    def initUI_main_selected(self, parent):
        parent.widgets = {'selectTree': ttk.Treeview(parent)}
        parent.widgets['selectTree'].pack(side=tk.LEFT, fill=tk.BOTH)

        tt = parent.widgets['selectTree']
        tt["columns"] = self.ctx.stat_fields
        tt.column("stype", width=80)
        tt.column("thr_min", width=60)
        tt.column("thr_max", width=60)
        tt.column("time_format", width=0)
        tt.heading("#0", text="Table Name")
        tt.heading("stype", text="Source Type")
        tt.heading("thr_min", text="Min. Thr.")
        tt.heading("thr_max", text="Max. Thr.")

    def initUI_btn(self, parent):

        parent.widgets = {'btn-fetch': Button(parent, text="Fetch", width=8, command=self.fetch_table_from_db),
                          'btn-clear': Button(parent, text="Clear", width=8, command=self.del_table_all),
                          'btn-loadf': Button(parent, text="Load from File", width=12, command=self.add_table_from_file)}

        parent.widgets['btn-fetch'].pack(side=tk.LEFT)
        parent.widgets['btn-clear'].pack(side=tk.RIGHT)
        parent.widgets['btn-loadf'].pack(side=tk.RIGHT)

    def fetch_table_from_db(self):
        """
        Get list of tables in database

        Context Inputs
        ---------------
        - frames['connect']
        - status
        - dbi

        Context Modifications
        ---------------------
        - dbi (update via connect.update_context())
        """

        self.ctx.update_context()

        #Check information is filled out
        for var in self.ctx.dbi_fields:
            if self.ctx.dbi[var] == '':
                self.ctx.status.set("Please enter in Database information")
                return

        #Attempt to fetch tables
        all_tables = core.hquery.get_all_tables(**self.ctx.dbi)

        #If failed, return error and return
        if all_tables == 0:
            logging.warning('FrameTable:fetch_table_from_db:failed to get table list for host:%s' %
                            self.ctx.dbi['host'])
            self.ctx.status.set("Failed to fetch table list")
            return

        #Update listbox
        wid = ViewModel.get_widget(self, ['main', 'fetched'],
                                 'fetchList')
        wid.delete(0, tk.END)
        for tab, col in enumerate(sorted(all_tables)):
            wid.insert(tab,col)

        wid.update_idletasks()
        self.ctx.status.set("Fetched")

    def add_table_selected(self):

        #Get the options for adding tables
        # main-opts frame
        values = {}
        for var in self.ctx.stat_fields:
            wid = ViewModel.get_widget(self, ['main', 'opts', var],
                                       var)
            values[var] = wid.get().strip()
            if values[var] == '':
                if var in self.ctx.stat_defaults:
                    values[var] = self.ctx.stat_defaults[var]
                else:
                    self.ctx.status.set("Please enter in %s info" % var)
                    return

        #Get the selected tables
        fetchList = ViewModel.get_widget(self, ['main', 'fetched'],
                                   'fetchList')
        selectTree = ViewModel.get_widget(self, ['main', 'selected'],
                                          'selectTree')

        #For each selected table
        selected_tables = [fetchList.get(idx) for idx in fetchList.curselection()]
        for col, tab in enumerate(selected_tables):

            #Remove table from selectTree if already exists
            if tab in self.ctx.tab_stat:
                self.clear_table(tab)

            #Add to selectTree
            selectTree.insert("",col, text=tab, values=values)

            #Add to context
            for var, val in values.iteritems():
                stat[var] = val
            self.ctx.add_table(tab, **stat)

    def add_table_from_file(self):

        user_open_req = filedialog.askopenfile()
        if not(user_open_req):
            return

        tab_stat = core.fetchInputs.table_stat(user_open_req.name)

        values = []
        for tab, stat in tab_stat.iteritems():
            for var in self.ctx.stat_fields:
                values.append(stat[var])

            selectTree = ViewModel.get_widget(self, ['main', 'selected'],
                                  'selectTree')
            selectTree.insert("", self.consts['selectTreeCount'],
                              text=tab, values=values)
            self.ctx.add_table(tab, **stat)
            self.consts['selectTreeCount'] += 1

    def del_table_all(self):

        selectTree = ViewModel.get_widget(self, ['main', 'selected'],
                                          'selectTree')

        for i in selectTree.get_children():
            table = selectTree.item(i)['text']
            self.ctx.del_table(table)
            selectTree.delete(i)

    def del_table_selected(self):

        selectTree = ViewModel.get_widget(self, ['main', 'selected'],
                                  'selectTree')
        curItem = selectTree.focus()
        table = curItem['text']
        self.ctx.del_table(table)
        selectTree.delete(curItem)

    def del_table(self, table_to_del):

        selectTree = ViewModel.get_widget(self, ['main', 'selected'],
                                          'selectTree')

        for i in selectTree.get_children():
            table = selectTree.item(i)['text']
            if table == table_to_del:
                self.ctx.del_table(table)
                selectTree.delete(i)
