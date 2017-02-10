import unittest
from sqlenergy.core import fetchInputs

class TableStat(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TableStat, self).__init__(*args, **kwargs)
        self.r = fetchInputs.table_stat('./tests/res/test_table_list.txt')

    def test_output_len(self):
        self.assertTrue(len(self.r) == 4)

    def test_output_full_row(self):
        self.assertTrue(self.r['full_row']['stype'] == 'renewable')
        self.assertTrue(self.r['full_row']['thr_min'] == -10.0)
        self.assertTrue(self.r['full_row']['thr_max'] == 10.0)
        self.assertTrue(self.r['full_row']['time_format'] == '%Y-%m-%d %H:%M:%S')

    def test_output_4_row(self):
        self.assertTrue(self.r['4_row']['stype'] == 'grid')
        self.assertTrue(self.r['4_row']['thr_min'] == 0.0)
        self.assertTrue(self.r['4_row']['thr_max'] == 1000.0)
        self.assertTrue(self.r['4_row']['time_format'] == '%Y-%m-%d %H:%M:%S.%f')

    def test_output_3_row(self):
        self.assertTrue(self.r['3_row']['stype'] == 'gas')
        self.assertTrue(self.r['3_row']['thr_min'] == 0.0)
        self.assertTrue(self.r['3_row']['thr_max'] == 100.0)
        self.assertTrue(self.r['3_row']['time_format'] == '%Y-%m-%d %H:%M:%S.%f')

    def test_output_2_row(self):
        self.assertTrue(self.r['2_row']['stype'] == 'grid')
        self.assertTrue(self.r['2_row']['thr_min'] == 0.0)
        self.assertTrue(self.r['2_row']['thr_max'] == 100.0)
        self.assertTrue(self.r['2_row']['time_format'] == '%Y-%m-%d %H:%M:%S.%f')

    def test_output_bad_row(self):
        with self.assertRaises(KeyError):
            self.r['bad_row']['stype']

    def test_types(self):
        all_types = list(set([self.r[k]['stype'] for k in self.r]))
        self.assertTrue(len(all_types) == 3)
        self.assertTrue('renewable' in all_types)
        self.assertTrue('grid' in all_types)
        self.assertTrue('gas' in all_types)
        self.assertTrue('solar' not in all_types)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
