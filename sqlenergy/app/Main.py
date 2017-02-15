import os
import logging
import Tkinter as tk
from Context import Context
from View import View
from ttk import *

class Main():
    def __init__(self):

        self.root = tk.Tk()
        self.context = Context()
        self.view = View(self.root, self.context)
        open('gui.main.log', 'w').close()#Clear the log file
        logging.basicConfig(filename='gui.main.log',level=logging.INFO)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    m = Main()
    m.run()
