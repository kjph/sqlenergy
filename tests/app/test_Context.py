import unittest
from sqlenergy.app.Context import Context

class ConfigureTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ConfigureTests, self).__init__(*args, **kwargs)
        self.TestObj = Context('./tests/res/app_test_Context_settings.ini')

    def test_types(self):
        """
        Test the correct types are loaded
        """

        types = self.TestObj.types
        self.assertTrue(len(types) == 3)

        for known_sect in ['dbi', 'stat', 'params']:
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

    def test_data_container(self):
        """
        Test the data container in context
        """

        self.assertTrue(len(self.TestObj.data) == len(self.TestObj.types))

        data = self.TestObj.data
        self.assertTrue(len(data) == 3)

        for known_sect in ['dbi', 'stat', 'params']:
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


def main():
    unittest.main()

if __name__ == '__main__':
    main()
