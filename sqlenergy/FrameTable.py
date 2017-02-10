import Tkinter as tk
import ttk
from Tkinter import Label, Frame, Listbox, Button, Entry
import tkFileDialog as filedialog
import hquery
import fetchInputs

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

        self.fetched_listbox = Listbox(self.main_frame, width=40, selectmode=tk.EXTENDED)
        self.fetched_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        #Build the select options (buttons between two listboxes)
        self.select_frame = Frame(self.main_frame)
        self.select_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.table_tree_count = 0
        self.initUI_select_frame(self.select_frame)

        self.table_tree = ttk.Treeview(self.main_frame)
        self.initUI_table_tree()
        self.table_tree.pack(side=tk.LEFT, fill=tk.BOTH)

        #Frame for containing buttons
        self.btn_frame = Frame(self)
        self.btn_frame.pack(fill=tk.X)
        self.initUI_btn_frame(self.btn_frame)

    def initUI_select_frame(self, parent):

        btn_size = 12

        self.select_type_frame = Frame(parent)
        self.select_type_frame.pack(fill=tk.X)

        self.select_thr_min_frame = Frame(parent)
        self.select_thr_min_frame.pack(fill=tk.X)

        self.select_thr_max_frame = Frame(parent)
        self.select_thr_max_frame.pack(fill=tk.X)

        self.select_type_lab = Label(self.select_type_frame, text="Source")
        self.select_type_lab.pack(side=tk.LEFT)
        self.select_type = Entry(self.select_type_frame, width=10)
        self.select_type.pack(side=tk.RIGHT)

        self.select_thr_min_lab = Label(self.select_thr_min_frame, text="Min. Thr.")
        self.select_thr_min_lab.pack(side=tk.LEFT)
        self.select_thr_min = Entry(self.select_thr_min_frame, width=10)
        self.select_thr_min.pack(side=tk.RIGHT)

        self.select_thr_max_lab = Label(self.select_thr_max_frame, text="Max. Thr.")
        self.select_thr_max_lab.pack(side=tk.LEFT)
        self.select_thr_max = Entry(self.select_thr_max_frame, width=10)
        self.select_thr_max.pack(side=tk.RIGHT)

        self.select_btn_add = Button(parent, text=">> Add", width=btn_size, command=self.add_tables)
        self.select_btn_add.pack()

        self.select_btn_del = Button(parent, text="<< Remove", width=btn_size)
        self.select_btn_del.pack(side=tk.BOTTOM)

        self.select_btn_add = Button(parent, text="Regex...", width=btn_size)
        self.select_btn_add.pack(side=tk.BOTTOM)

        self.select_btn_add = Button(parent, text="Select All", width=btn_size)
        self.select_btn_add.pack(side=tk.BOTTOM)

    def initUI_btn_frame(self, parent):

        self.btn_fetch_list = Button(parent, text="Fetch", width=8, command=self.fetch_tables)
        self.btn_fetch_list.pack(side=tk.LEFT)

        self.btn_sel_all = Button(parent, text="Clear", width=8, command=self.clear_tables)
        self.btn_sel_all.pack(side=tk.RIGHT)

        self.btn_sel_all = Button(parent, text="Load from File", width=12, command=self.load_tables)
        self.btn_sel_all.pack(side=tk.RIGHT)

    def initUI_table_tree(self):
        #See: http://knowpapa.com/ttk-treeview/
        self.table_tree["columns"] = ("type", "thr_min", "thr_max")
        self.table_tree.column("type", width=100)
        self.table_tree.column("thr_min", width=60)
        self.table_tree.column("thr_max", width=60)
        self.table_tree.heading("#0", text="Table Name")
        self.table_tree.heading("type", text="Source Type")
        self.table_tree.heading("thr_min", text="Min. Thr.")
        self.table_tree.heading("thr_max", text="Max. Thr.")

    def fetch_tables(self):

        if self.ctx.last_conn:
            self.fetched_listbox.delete(0, tk.END)
            all_tables = hquery.get_all_tables(**self.ctx.dbi)
            for tab, col in enumerate(sorted(all_tables)):
                self.fetched_listbox.insert(tab,col)

            self.fetched_listbox.update_idletasks()
        else:
            self.ctx.status.set("Please test connection first")

    def add_tables(self):

        source_type = self.select_type.get().strip()
        thr_min = self.select_thr_min.get().strip()
        thr_max = self.select_thr_max.get().strip()
        time_format = '%Y-%m-%d %H:%M:%S.%f'

        if thr_min == '':
            thr_min = 0.0
        if thr_max == '':
            thr_max = 100

        thr_min = float(thr_min)
        thr_max = float(thr_max)

        if source_type != '':
            selected_tables = [self.fetched_listbox.get(idx) for idx in self.fetched_listbox.curselection()]
            for col, tab in enumerate(selected_tables):
                if tab in self.ctx.tab_stat:
                    self.clear_table(tab)
                self.table_tree.insert("", col, text=tab, values=(source_type, thr_min, thr_max))
                stat = {'stype': source_type, 'thr_min': thr_min,
                        'thr_max': thr_max, 'time_format': time_format}
                self.ctx.add_table(tab, **stat)

    def load_tables(self):

        user_open_req = filedialog.askopenfile()
        if not(user_open_req):
            return

        tab_stat = fetchInputs.table_stat(user_open_req.name)


        for tab, stat in tab_stat.iteritems():
            source_type = stat['stype']
            thr_min = stat['thr_min']
            thr_max = stat['thr_max']

            self.table_tree.insert("", self.table_tree_count, text=tab, values=(source_type, thr_min, thr_max))
            self.ctx.add_table(tab, **stat)
            self.table_tree_count += 1

    def clear_tables(self):
        for i in self.table_tree.get_children():
            table = self.table_tree.item(i)['text']
            self.ctx.del_table(table)
            self.table_tree.delete(i)

    def clear_table(self, table_to_del):
        for i in self.table_tree.get_children():
            table = self.table_tree.item(i)['text']
            if table == table_to_del:
                self.ctx.del_table(table)
                self.table_tree.delete(i)

