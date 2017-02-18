import os
import logging
import Tkinter as tk
from ttk import *
from Context import Context
from View import View

class Main():
    """
    Creates an instance of the application
    """

    def __init__(self, conf_last='.conf/last.ini', conf_ctx='.conf/settings.ini'):

        #Configure the log file
        log_file = 'gui.main.log'
        open(log_file, 'w').close()#Clear the log file
        logging.basicConfig(filename=log_file,level=logging.INFO)

        self.root = tk.Tk()
        self.ctx = Context(conf_ctx)

        #Load configuration if it exists
        if os.path.isfile(conf_last):
            self.ctx.load_context(conf_last)

        self.view = View(self.root, self.ctx)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    m = Main()
    m.run()
