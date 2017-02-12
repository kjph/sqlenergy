import os
import logging
import Tkinter as tk
from Context import Context
from View import View

class Main():
    def __init__(self):

        self.root = tk.Tk()
        self.context = Context()
        self.view = View(self.root, self.context)
        logging.basicConfig(filename='gui.main.log',level=logging.DEBUG)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    m = Main()
    m.run()
