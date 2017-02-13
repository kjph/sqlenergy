import os
import logging
import collections

class Context():

    def __init__(self):

        #Frame container
        #TODO: is this needed?
        self.frames = {}

        #Specify immutable object
        #That defines the structure of Core Model Attributes
        self.dbi_fields = ('host', 'user', 'passwd', 'db', 'port')
        self.dbi_defaults = {'port': 3306}
        self.stat_fields = (('stype', "Source Type"),
                            ('thr_min', "Thr. Min"),
                            ('thr_max', "Thr. Max"),
                            ('time_format', 'Time Form.'))
        self.stat_defaults = {'thr_min': 0.0,
                              'thr_max': 100.0,
                              'time_format': '%Y-%m-%d %H:%M:%S.%f'}
        self.param_list = ('outf_dir', 'outf_name', 'start_date', 'end_date', 'outf_ext')

        #Core Model Attributes
        self.dbi = {x: None for x in self.dbi_fields}
        self.tab_stat = collections.defaultdict(dict)
        self.params = {x: None for x in self.param_list}

        self.params['outf_dir'] = os.path.expanduser("~")
        self.params['outf_name'] = 'sqlenergy_output'
        self.params['outf_ext'] = '.csv'

        #ViewModel function handles
        self.func = []
        self.funcgroup = collections.defaultdict(list)

    def add_table(self, table, **stat):

        if len(stat) != len(self.stat_fields):
            logging.warning("CTX:ERR:Attempted to add table in bad format")
            return
        for field in self.stat_fields:
            if field not in stat:
                logging.warning("CTX:ERR:Attempted to add table in bad format")
                return
        self.tab_stat[table] = stat
        logging.debug("CTX:add_table:%s:%s" % (table,stat))

    def del_table(self, table):
        self.tab_stat[table] = {}
        self.tab_stat.pop(table, None)
        logging.debug("CTX:del_table:%s" % table)

    def update_context(self):
        r = 1
        for f in self.func:
            r = r and f.__func__()
        return r

    def on_call(self, call):

        for f in self.funcgroup[call]:
            f.__func__()
