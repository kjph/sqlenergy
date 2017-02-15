import os
import logging
import ConfigParser
import Tkinter as tk
from Context import Context
from View import View
from ttk import *

class Main():
    def __init__(self):

        self.root = tk.Tk()
        self.context = Context()

        #Load configuration
        if os.path.isfile('.conf/last.ini'):
            conf = ConfigParser.ConfigParser()
            conf.readfp(open('.conf/last.ini'))
            if not(conf.getboolean('core', 'load')):
                conf = None

        self.view = View(self.root, self.context, conf)
        open('gui.main.log', 'w').close()#Clear the log file
        logging.basicConfig(filename='gui.main.log',level=logging.INFO)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    m = Main()
    m.run()
