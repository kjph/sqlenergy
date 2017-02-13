import logging
from datetime import datetime
import Tkinter as tk
from Tkinter import Frame, Label, Entry, Button
import tkFileDialog as filedialog
import ViewModel
from ttk import *

class FrameSet(tk.Frame):
    """
    Frame for sending the query
    """

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.ctx = ctx
        ViewModel.set_update_func(ctx, staticmethod(self.update_context))
        ViewModel.add_func_group(ctx, staticmethod(self.clear_all), "clearAll")

        self.strvars = {'outf_dir': tk.StringVar(value="%s" % self.ctx.params['outf_dir']),
                        'outf_name': tk.StringVar(value="%s" % self.ctx.params['outf_name'])}

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(self, ['top', 'main'],
                       **{'fill': tk.BOTH})

        f = ViewModel.get_frame(self, 'top')
        self.initUI_top(f)

        f = ViewModel.get_frame(self, 'main')
        self.initUI_main(f)

    def initUI_top(self, parent):
        parent.widgets = {'desp': Label(parent, text="Settings",
                                        font=self.ctx.const['font_title'])}
        parent.widgets['desp'].pack(anchor=tk.W)

    def initUI_main(self, parent):

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(parent, ['set', 'btn'],
                       **{'fill': tk.BOTH, 'side': tk.LEFT})

        #Sub frames under 'set'
        f_set = ViewModel.get_frame(parent, 'set')
        ViewModel.mk_frames_in(f_set, ['date', 'file'],
                               **{'fill': tk.BOTH})

        self.initUI_main_btn(ViewModel.get_frame(parent, 'btn'))
        self.initUI_main_set_date(ViewModel.get_frame(parent, ['set', 'date']))
        self.initUI_main_set_file(ViewModel.get_frame(parent, ['set', 'file']))

    def initUI_main_set_date(self, parent):

        parent.widgets = {'start-lab':      Label(parent, text="Start Date:"),
                          'start-y-lab':    Label(parent, text="Y"),
                          'start-y':        Entry(parent, width=5),
                          'start-m-lab':    Label(parent, text="M"),
                          'start-m':        Entry(parent, width=3),
                          'start-d-lab':    Label(parent, text="D"),
                          'start-d':        Entry(parent, width=3),
                          'end-lab':        Label(parent, text="End Date:"),
                          'end-y-lab':      Label(parent, text="Y"),
                          'end-y':          Entry(parent, width=5),
                          'end-m-lab':      Label(parent, text="M"),
                          'end-m':          Entry(parent, width=3),
                          'end-d-lab':      Label(parent, text="D"),
                          'end-d':          Entry(parent, width=3),
                          'min-res-lab':    Label(parent, text="Minute Res."),
                          'min-res':        Entry(parent, width=5)}

        packing = [('start-lab',   {'side':tk.LEFT}),
                   ('start-y-lab', {'side':tk.LEFT}),
                   ('start-y',     {'side':tk.LEFT, 'padx': (0,5)}),
                   ('start-m-lab', {'side':tk.LEFT}),
                   ('start-m',     {'side':tk.LEFT, 'padx': (0,5)}),
                   ('start-d-lab', {'side':tk.LEFT}),
                   ('start-d',     {'side':tk.LEFT, 'padx': (0,30)}),
                   ('end-lab',     {'side':tk.LEFT}),
                   ('end-y-lab',   {'side':tk.LEFT}),
                   ('end-y',       {'side':tk.LEFT, 'padx': (0, 5)}),
                   ('end-m-lab',   {'side':tk.LEFT}),
                   ('end-m',       {'side':tk.LEFT, 'padx': (0, 5)}),
                   ('end-d-lab',   {'side':tk.LEFT}),
                   ('end-d',       {'side':tk.LEFT}),
                   ('min-res',     {'side':tk.RIGHT}),
                   ('min-res-lab', {'side':tk.RIGHT})
                   ]
        ViewModel.pack_widgets(parent.widgets, packing)

    def initUI_main_set_file(self, parent):

        parent.widgets = {'dir-label':      Label(parent, text="Output Directory:"),
                          'dir-current':    tk.Entry(parent, textvariable=self.strvars['outf_dir'],
                                                  state="readonly", width=45,
                                                  bd=2),
                          'dir-btn':        Button(parent, text="...", command=self.set_output_dir,
                                                   width=5),
                          'file-label':     Label(parent, text="Filename:"),
                          'file-entry':     Entry(parent, width=30, textvariable=self.strvars['outf_name'])}

        packing = [('dir-label',    {'side': tk.LEFT}),
                   ('dir-current',  {'side': tk.LEFT}),
                   ('file-entry',   {'side': tk.RIGHT}),
                   ('file-label',   {'side': tk.RIGHT}),
                   ('dir-btn',      {'side': tk.RIGHT})]
        ViewModel.pack_widgets(parent.widgets, packing)

    def initUI_main_btn(self, parent):
        parent.widgets = {'clear':  Button(parent, text="Clear", width=8, command=self.clear_all)}

        packing = [('clear',    {'side': tk.BOTTOM})]
        ViewModel.pack_widgets(parent.widgets, packing)

    def set_output_dir(self):
        """
        Open filedialog for user to set output directory
        """

        user_dir_req = filedialog.askdirectory(title="Select Output Directory",
                                               **self.ctx.opts['dir'])
        if not(user_dir_req):
            return

        self.ctx.params['outf_dir'] = user_dir_req
        self.strvars['outf_dir'].set(user_dir_req)
        logging.debug("FrameQuery:set_output_directory:%s" % self.ctx.params['outf_dir'])

        self.update_context()

    def update_context(self, clear=False):

        outf_name = ViewModel.get_widget(self, ['main', 'set', 'file'],
                                         'file-entry').get().strip()

        f = ViewModel.get_frame(self, ['main', 'set', 'date'])
        widgets = f.widgets
        dates = {'start_y': widgets['start-y'].get().strip(),
                 'start_m': widgets['start-m'].get().strip(),
                  'start_d': widgets['start-d'].get().strip(),
                  'end_y': widgets['end-y'].get().strip(),
                  'end_m': widgets['end-m'].get().strip(),
                  'end_d': widgets['end-d'].get().strip()}

        max_yr = datetime.now().year
        date_thres = {'start_y': (0, max_yr),
                      'start_m': (1, 12),
                      'start_d': (1, 31),
                      'end_y': (0, max_yr),
                      'end_m': (1, 12),
                      'end_d': (1, 31)}

        for key, val in dates.iteritems():
            if val == None:
                continue
            if not(val.isdigit()):
                self.ctx.status.set("Please enter in numeric values")
                return 0
            else:
                dates[key] = int(val)

            if val < date_thres[key][0]:
                self.ctx.status.set("%s is less than its threshold of %i" % (key, date_thres[key][0]))
                return 0
            if val > date_thres[key][1]:
                 self.ctx.status.set("%s is greater than its threshold of %i" % (key, date_thres[key][1]))

        self.ctx.params['start_date'] = "%s-%s-%s" % (dates['start_y'], dates['start_m'], dates['start_d'])
        self.ctx.params['end_date'] = "%s-%s-%s" % (dates['end_y'], dates['end_m'], dates['end_d'])

    def clear_all(self):
        """
        Remove all information from this Frame
        """

        f = ViewModel.get_frame(self, ['main', 'set', 'date'])
        widgets = f.widgets
        widgets['start-y'].delete(0, 'end')
        widgets['start-m'].delete(0, 'end')
        widgets['start-d'].delete(0, 'end')
        widgets['end-y'].delete(0, 'end')
        widgets['end-m'].delete(0, 'end')
        widgets['end-d'].delete(0, 'end')
        ViewModel.get_widget(self, ['main', 'set', 'file'],
                             'file-entry').delete(0, 'end')
        self.update_context(True)
