import unittest
from sqlenergy.app.Context import Context

class ConfigureTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ConfigureTests, self).__init__(*args, **kwargs)
        self.TestObj = Context('./tests/res/app_test_Context_settings.ini')
        self.expected_sections = ['dbi', 'stat', 'params', 'control']

    def test_types(self):
        """
        Test the correct types are loaded
        """

        types = self.TestObj.types
        self.assertTrue(len(types) == len(self.expected_sections))

        for known_sect in self.expected_sections:
            self.assertTrue(known_sect in types)

        #Database info test
        self.assertTrue(len(types['dbi']) == 5)
        self.assertTrue(types['dbi']['host'] == str)
        self.assertTrue(types['dbi']['user'] == str)
        self.assertTrue(types['dbi']['passwd'] == str)
        self.assertTrue(types['dbi']['db'] == str)
        self.assertTrue(types['dbi']['port'] == int)

        #params random test
        self.assertTrue(types['params']['min_res'] == float)

        #Control
        self.assertTrue(types['control']['save'] == int)

    def test_data_container(self):
        """
        Test the data container in context
        """

        self.assertTrue(len(self.TestObj.data) == len(self.TestObj.types))

        data = self.TestObj.data
        self.assertTrue(len(data) == len(self.expected_sections))

        for known_sect in self.expected_sections:
            self.assertTrue(known_sect in data)

    def test_data_values(self):

        data = self.TestObj.data

        #Test loaded values
        self.assertTrue(data['dbi']['host'] == None)
        self.assertTrue(data['dbi']['user'] == None)
        self.assertTrue(data['dbi']['port'] == 3306)
        self.assertTrue(data['stat']['thr_min'] == 0.0)
        self.assertTrue(data['stat']['thr_max'] == 100.0)
        self.assertTrue(data['stat']['time_format'] == '%Y-%m-%d %H:%M:%S.%f')

    def test_disp(self):

        dispStrs = self.TestObj.dispStrs

        self.assertTrue(len(dispStrs) == 3)

        #Test loaded values
        self.assertTrue(dispStrs['dbi']['host'] == 'Host')
        self.assertTrue(dispStrs['dbi']['db'] == 'Database')
        self.assertTrue(dispStrs['stat']['thr_min'] == 'Min. Val')
        with self.assertRaises(KeyError):
            dispStrs['params']['outf_ext']

    def test_layout(self):

        layout = self.TestObj.layout

        self.assertTrue(len(layout) == 1)

        self.assertTrue(len(layout['dbi']) == 3)

        exp_layout = [['host'], ['user', 'passwd'], ['db', 'port']]
        self.assertTrue(layout['dbi'] == exp_layout)

class LoadContextTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(LoadContextTests, self).__init__(*args, **kwargs)
        self.TestObj = Context('./tests/res/app_test_Context_settings.ini')
        self.TestObj.load_context('./tests/res/app_test_Context_last.ini')
        self.expected_sections = ['dbi', 'stat', 'params', 'control']

    def test_is_file_fail(self):
        """
        Test a non-file will not overwrite current context and a false returns
        """

        r = self.TestObj.load_context('./this/is/not/a/path')
        self.assertFalse(r)

        r = self.TestObj.load_context('./tests/res/app_test_Context_last_badLoad.ini')
        self.assertFalse(r)

        r = self.TestObj.load_context('./tests/res/app_test_Context_last_noLoad.ini')
        self.assertFalse(r)

    def test_values(self):
        """
        Test the values are loaded
        """

        data = self.TestObj.data
        self.assertTrue(len(data) == len(self.expected_sections))

        for known_sect in ['dbi', 'stat', 'params']:
            self.assertTrue(known_sect in data)

        #Database info values
        self.assertTrue(data['dbi']['host'] == '111.222.333.444')
        self.assertTrue(data['dbi']['user'] == 'someUser')
        self.assertTrue(data['dbi']['passwd'] == '%^&_pass_with!@#$_complx,chars!:=**()/')
        self.assertTrue(data['dbi']['db'] == 'database')
        self.assertTrue(data['dbi']['port'] == 3306)

        #tab stat
        self.assertTrue(data['stat']['file'] == '.conf/last_tabstat.txt')

        #params
        self.assertTrue(data['params']['start_date'] == '2016-01-01')
        self.assertTrue(data['control']['save'])

    def test_bad_values(self):

        data = self.TestObj.data

        with self.assertRaises(KeyError):
            data['dbi']['doNotAdd']
            data['notASect']


def main():
    unittest.main()

if __name__ == '__main__':
    main()
