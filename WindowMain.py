import Tkinter as tk
from Tkinter import Label, Frame
from FrameConnect import FrameConnect
from FrameTable import FrameTable
from FrameSet import FrameSet

class Context():

    def __init__(self):
        self.dbi = {'host': None, 'user': None, 'passwd': None, 'db': None, 'port': 3306}

class WindowMain(tk.Frame):
    """
    Primary container
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        #Title
        self.parent = parent
        self.parent.title("CSIRO Energy Analyzer")

        #Context container to pass to children
        self.ctx = Context()
        self.ctx.status = tk.StringVar(value="Ready.")
        self.ctx.global_config = {'padx': 5, 'pady': 5}

        #Master Frame to contain main widgets
        self.main = Frame(self.parent)
        self.main.pack()

        #Status bar
        self.status_label = Label(self.parent, textvariable=self.ctx.status, font="Default 8")
        self.status_label.pack(anchor=tk.W)

        self.create_ui()

    def create_ui(self):
        #UI Layout
        self.main_connect_label = Label(self.main, text="test")

        self.main_connect = FrameConnect(self.main, self.ctx, bd=3, relief=tk.GROOVE)
        self.main_connect.pack(side=tk.LEFT, fill=tk.BOTH)

        self.main_table = FrameTable(self.main, self.ctx.status, bd=3, relief=tk.GROOVE)
        self.main_table.pack(side=tk.LEFT, fill=tk.BOTH)

        self.main_table = FrameSet(self.main, self.ctx, bd=3, relief=tk.GROOVE)
        self.main_table.pack(side=tk.LEFT, fill=tk.BOTH)


if __name__ == '__main__':
    root = tk.Tk()
    WindowMain(root)
    root.mainloop()
