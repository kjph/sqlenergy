import ntpath
import Tkinter as tk
from Tkinter import Label, Button, Entry, Listbox
import tkFileDialog as filedialog

class MainApplication(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.master.title("CSIRO Energy 8")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)

        #Init variables
        self.data_file = None
        self.idx_current_head = []

        #Grid management
        file_row, file_col = [1, 0]
        host_row, host_col = [2, 0]
        cred_row, cred_col = [3, 0]
        db_row, db_col = [4, 0]

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

    def load_file(self):
        user_open_req = filedialog.askopenfile()
        if user_open_req:
            self.data_file = user_open_req.name
            self.file_current_name.set(ntpath.basename(self.data_file))
            self.fill_idx()

    def fill_idx(self):
        self.idx_sa2.delete(0, tk.END)
        if self.data_file != None:
            for idx, col in enumerate(guiFunc.get_csv_header(self.data_file)):
                self.idx_sa2.insert(idx, col)

        self.idx_sa2.update_idletasks()


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)#.grid(side="top", fill="both", expand=True)
    root.mainloop()
