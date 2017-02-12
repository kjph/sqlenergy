import logging
import Tkinter as tk
from Tkinter import Frame, Label, Entry, Button
import tkFileDialog as filedialog
import ViewModel

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

        self.strvars = {'outputDir': tk.StringVar(value="")}

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
                          'end-d':          Entry(parent, width=3)}

        packing = [('start-lab',   {'side':tk.LEFT}),
                   ('start-y-lab', {'side':tk.LEFT}),
                   ('start-y',     {'side':tk.LEFT}),
                   ('start-m-lab', {'side':tk.LEFT}),
                   ('start-m',     {'side':tk.LEFT}),
                   ('start-d-lab', {'side':tk.LEFT}),
                   ('start-d',     {'side':tk.LEFT}),
                   ('end-d',       {'side':tk.RIGHT}),
                   ('end-d-lab',   {'side':tk.RIGHT}),
                   ('end-m',       {'side':tk.RIGHT}),
                   ('end-m-lab',   {'side':tk.RIGHT}),
                   ('end-y',       {'side':tk.RIGHT}),
                   ('end-y-lab',   {'side':tk.RIGHT}),
                   ('end-lab',     {'side':tk.RIGHT})]
        ViewModel.pack_widgets(parent.widgets, packing)

    def initUI_main_set_file(self, parent):

        parent.widgets = {'dir-label':      Label(parent, text="Output Directory:"),
                          'dir-current':    Entry(parent, textvariable=self.strvars['outputDir'],
                                                  state="readonly", width=45),
                          'dir-btn':        Button(parent, text="...", command=self.set_output_dir),
                          'file-label':     Label(parent, text="Filename:"),
                          'file-entry':     Entry(parent, width=30)}

        packing = [('dir-label',    {'side': tk.LEFT}),
                   ('dir-current',  {'side': tk.LEFT}),
                   ('file-entry',   {'side': tk.RIGHT}),
                   ('file-label',   {'side': tk.RIGHT}),
                   ('dir-btn',      {'side': tk.RIGHT})]
        ViewModel.pack_widgets(parent.widgets, packing)

    def initUI_main_btn(self, parent):
        parent.widgets = {'clear':  Button(parent, text="Clear", width=8)}

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
        self.strvars['outputDir'].set(user_dir_req)
        logging.debug("FrameQuery:set_output_directory:%s" % self.ctx.output_dir)

        self.update_context()

    def update_context(self):
        self.ctx.params['outf_name'] = ViewModel.get_widget(self, ['main', 'set', 'file'],
                                                            'file-entry').get().strip()

        f = ViewModel.get_frame(self, ['main', 'set', 'date'])
        widgets = f.widgets
        self.ctx.params['start_date'] = "%s-%s-%s" % (widets['start-y'].get().strip(),
                                                      widets['start-m'].get().strip(),
                                                      widets['start-d'].get().strip())
        self.ctx.params['end_date'] = "%s-%s-%s" % (widets['end-y'].get().strip(),
                                                    widets['end-m'].get().strip(),
                                                    widets['end-d'].get().strip())

    def clear_all(self):
        pass
