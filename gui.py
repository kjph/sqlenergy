import ntpath
import Tkinter as tk
from Tkinter import Label, Button, Entry, Listbox
import tkFileDialog as filedialog
import fetchInputs

class MainApplication(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.master.title("CSIRO Energy 8")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)

        #Init variables
        self.data_file = None
        self.table_current = []

        #Grid management
        file_row, file_col = [1, 0]
        host_row, host_col = [2, 0]
        cred_row, cred_col = [3, 0]
        db_row, db_col = [4, 0]
        date_row, date_col = [5, 0]
        table_row, table_col = [1, 5]
        table_row_span, table_col_span = [8, 4]

        #File
        self.file_current_name = tk.StringVar()
        self.file_current_name.set('None')

        self.file_label = Label(master, text="Config File:")
        self.file_label.grid(row=file_row, column=file_col, sticky='E')

        self.file_current = Label(master, textvariable=self.file_current_name)
        self.file_current.grid(row=file_row, column=file_col+1)

        self.file_button = Button(master, text="Browse", command=self.load_file, width=10)
        self.file_button.grid(row=file_row, column=file_col+3, sticky='W')

        #Host
        self.host_label = Label(master, text="Host:")
        self.host_label.grid(row=host_row, column=host_col, sticky='E')

        self.host_entry = Entry(master)
        self.host_entry.grid(row=host_row, column=host_col+1, sticky='W')

        #Cred
        self.user_label = Label(master, text="User:")
        self.user_label.grid(row=cred_row, column=cred_col, sticky='E')

        self.user_entry = Entry(master)
        self.user_entry.grid(row=cred_row, column=cred_col+1, sticky='W')

        self.passwd_label = Label(master, text="Passwd:")
        self.passwd_label.grid(row=cred_row, column=cred_col+2, sticky='E')

        self.passwd_entry = Entry(master)
        self.passwd_entry.grid(row=cred_row, column=cred_col+3, sticky='W')

        #db
        self.db_label = Label(master, text="Database:")
        self.db_label.grid(row=db_row, column=db_col, sticky='E')

        self.user_entry = Entry(master)
        self.user_entry.grid(row=db_row, column=db_col+1, sticky='W')

        self.passwd_label = Label(master, text="Port:")
        self.passwd_label.grid(row=db_row, column=db_col+2, sticky='E')

        self.passwd_entry = Entry(master)
        self.passwd_entry.grid(row=db_row, column=db_col+3, sticky='W')

        #dates
        self.date_start_label = Label(master, text="Start")
        self.date_end_label = Label(master, text="End")
        self.date_year_label = Label(master, text="Year:")
        self.date_month_label = Label(master, text="Month:")
        self.date_day_label = Label(master, text="Day:")

        self.date_start_label.grid(row=date_row, column=date_col+1, sticky='E')
        self.date_end_label.grid(row=date_row, column=date_col+3, sticky='E')
        self.date_year_label.grid(row=date_row+1, column=date_col, sticky='E')
        self.date_month_label.grid(row=date_row+2, column=date_col, sticky='E')
        self.date_day_label.grid(row=date_row+3, column=date_col, sticky='E')

        self.date_start_year_entry = Entry(master)
        self.date_start_month_entry = Entry(master)
        self.date_start_day_entry = Entry(master)

        self.date_start_year_entry.grid(row=date_row+1, column=date_col+1)
        self.date_start_month_entry.grid(row=date_row+2, column=date_col+1)
        self.date_start_day_entry.grid(row=date_row+3, column=date_col+1)

        self.date_end_year_entry = Entry(master)
        self.date_end_month_entry = Entry(master)
        self.date_end_day_entry = Entry(master)

        self.date_end_year_entry.grid(row=date_row+1, column=date_col+3)
        self.date_end_month_entry.grid(row=date_row+2, column=date_col+3)
        self.date_end_day_entry.grid(row=date_row+3, column=date_col+3)

        #Tables
        self.table_label = Label(master, text="Select Tables to Pull:")
        self.table_label.grid(row=table_row, column=table_col, sticky='W')

        self.table_listbox = Listbox(master, listvariable=self.table_current, width=50,
                                     selectmode = tk.EXTENDED)
        self.table_listbox.grid(row=table_row+1, column=table_col, columnspan=table_col_span, rowspan=table_row_span)
        self.fill_idx()

    def load_file(self):
        user_open_req = filedialog.askopenfile()
        if user_open_req:
            self.data_file = user_open_req.name
            self.file_current_name.set(ntpath.basename(self.data_file))
            self.fill_idx()

    def fill_idx(self):
        self.table_listbox.delete(0, tk.END)
        for name, col in enumerate(fetchInputs.table_names('res/table_list.txt')):
            self.table_listbox.insert(name, col)

        self.table_listbox.update_idletasks()


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)#.grid(side="top", fill="both", expand=True)
    root.mainloop()
