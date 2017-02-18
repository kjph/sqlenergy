import os
import logging
import collections
import ConfigParser

class Context():

    def __init__(self, config_file):

        #Frame container
        #TODO: is this needed?
        self.frames = {}
        self.types = {}
        self.data = {}
        self.dispStrs = {}
        self.defaults = {}
        self.layout = {}
        self._configure(config_file)

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
        self.param_list = ('outf_dir', 'outf_name', 'start_date', 'end_date', 'outf_ext', 'min_res')
        self.param_defaults = {'min_res': 15}

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

    def _configure(self, config_file):
        """
        Configure the context class.

        This method ensures the correct types are used in the app
        """

        conf = ConfigParser.ConfigParser()
        conf.readfp(open(config_file))

        #Load type information
        for sect in conf.sections():
            if '-types' in sect:
                key = sect.replace('-types', '')
                self.types[key] = {i:eval(conf.get(sect, i)) for i in conf.options(sect)}
                self.data[key] = {i:None for i in conf.options(sect)}
            if '-disp' in sect:
                key = sect.replace('-disp', '')
                self.dispStrs[key] = {i:conf.get(sect, i) for i in conf.options(sect)}
            if '-layout' in sect:
                key = sect.replace('-layout', '')
                self.layout[key] = [[x.strip() for x in conf.get(sect, i).split(',')] for i in conf.options(sect)]

        #Second 'run'
        #Have to make sure all types are loaded first
        self.defaults = collections.defaultdict(dict)
        for sect in conf.sections():
            if '-defaults' in sect:
                key = sect.replace('-defaults', '')
                for i in conf.options(sect):
                    caster = self.types[key][i]
                    self.defaults[key][i] = caster(conf.get(sect, i))

        #Fill the containers with defaults
        for sect, container in self.data.iteritems():
            for key in container:
                if key in self.defaults[sect]:
                    container[key] = self.defaults[sect][key]

    def load_context(self, config_file):
        """
        Load context from a .INI config file
        """

        if os.path.isfile(config_file):
            conf = ConfigParser.ConfigParser()
            conf.readfp(open(config_file))
        else:
            return 0

        if 'control' not in conf.sections():
            logging.warning("CTX:load_context:No control section found. Returning")
            return 0
        else:
            if conf.get('control', 'save') == '0':
                return 0

        for sect in conf.sections():
            if sect in self.types:
                for i in conf.options(sect):
                    if i in self.types[sect]:
                        caster = self.types[sect][i]

                        try:
                            self.data[sect][i] = caster(conf.get(sect, i))
                        except ValueError:
                            logging.warning("CTX:load_context:bad type in %s for key %s" % (sect, i))
                    else:
                        logging.warning("CTX:load_context:no type specified for %s,%s. Casting to string" % (sect, i))
                        self.data[sect][i] = str(conf.get(sect, i))
            else:
                logging.warning("CTX:load_context:Detected sect=%s no found in Configured Context" % sect)

        return 1

    def add_table(self, table, **stat):

        if len(stat) != len(self.stat_fields):
            logging.warning("CTX:ERR:Attempted to add table in bad format")
            return
        for field in [x[0] for x in self.stat_fields]:
            if field not in stat:
                logging.warning("CTX:ERR:Attempted to add table in bad format")
                return
            if field == 'thr_min' or field == 'thr_max':
                stat[field] = float(stat[field])
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
