import os
import Tkinter as tk
from Tkinter import Frame, Label, Button
import ViewModel
from . import core

class FrameQuery(tk.Frame):

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.ctx = ctx

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(self, ['top', 'main'],
                       **{'fill': tk.BOTH, 'side': tk.LEFT})

        f = ViewModel.get_frame(self, 'top')
        self.initUI_top(f)

        f = ViewModel.get_frame(self, 'main')
        f.pack(side=tk.RIGHT)#Repack main class
        self.initUI_main(f)

    def initUI_top(self, parent):

        parent.widgets = {'desp': Label(parent, text="Run Query",
                                        font=self.ctx.const['font_title'])}
        parent.widgets['desp'].pack(anchor=tk.W)

    def initUI_main(self, parent):

        parent.widgets = {'clear-all':  Button(parent, text="Clear All", command=self.clear_all),
                          'query':      Button(parent, text="Query", command=self.do_query)}
        packing = [('clear-all', {'side': tk.LEFT}),
                   ('query', {'side': tk.LEFT})]
        ViewModel.pack_widgets(parent.widgets, packing)

    def clear_all(self):
        self.ctx.on_call('clearAll')

    def do_query(self):
        self.ctx.update_context()

        min_res = 15
        Series = core.hquery.get_time_series(self.ctx.params['start_date'],
                                 self.ctx.params['end_date'],
                                 min_res,
                                 self.ctx.tab_stat,
                                 **self.ctx.dbi)

        #Write output
        outf = os.path.join(self.ctx.params['outf_dir'], self.ctx.params['outf_name'])
        with open(outf, 'w') as fd:
            fd.write(str(Series))
