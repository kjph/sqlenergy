import os
import Tkinter as tk
from Tkinter import Frame, Label, Button
import ViewModel
from sqlenergy import core
from sqlenergy import plot
from ttk import *

class FrameQuery(tk.Frame):

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.ctx = ctx

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(self, [('top', {'fill': tk.BOTH, 'side': tk.LEFT}),
                                      ('main', {'fill': tk.BOTH, 'side': tk.RIGHT})])

        f = ViewModel.get_frame(self, 'top')
        self.initUI_top(f)

        f = ViewModel.get_frame(self, 'main')
        self.initUI_main(f)

    def initUI_top(self, parent):

        parent.widgets = {'desp': Label(parent, text="Run Query",
                                        font=self.ctx.const['font_title'])}
        parent.widgets['desp'].pack()

    def initUI_main(self, parent):

        parent.widgets = {'clear-all':  Button(parent, text="Clear All", command=self.clear_all),
                          'query':      Button(parent, text="Query", command=self.do_query)}

        packing = [('clear-all', {'side': tk.LEFT}),
                   ('query', {'side': tk.LEFT})]
        ViewModel.pack_widgets(parent.widgets, packing, self.ctx.global_widget_conf)

    def clear_all(self):
        self.ctx.on_call('clearAll')

    def do_query(self):
        """
        Get all context information and attempt query
        """

        r = self.ctx.update_context()
        if not(r):
            self.ctx.status.set("something went wrong")
            return 0

        self.ctx.status.set("Running Query...")

        min_res = 15
        Series = core.hquery.get_time_series(self.ctx.params['start_date'],
                                 self.ctx.params['end_date'],
                                 self.ctx.params['min_res'],
                                 self.ctx.tab_stat,
                                 **self.ctx.dbi)

        if Series == 0:
            self.ctx.status.set("Query failed")
            return

        #Write output
        outf = os.path.join(self.ctx.params['outf_dir'], self.ctx.params['outf_name'] + self.ctx.params['outf_ext'])
        with open(outf, 'w') as fd:
            fd.write(str(Series))

        plot.test.plot_time_series(Series)

        self.ctx.status.set("Query Complete")
