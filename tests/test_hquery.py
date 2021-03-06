import unittest
from sqlenergy.core import hquery, fetchInputs

class GetTimeSeriesTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GetTimeSeriesTest, self).__init__(*args, **kwargs)
        dbi = fetchInputs.database_inputs('./cred.json')
        print dbi
        tab_stat = fetchInputs.table_stat('./tests/res/test_table_list.txt')
        self.TestSeries = hquery.get_time_series('2016-01-01', '2016-01-02', 15,
                                                 tab_stat, **dbi)

    def test_return_class_stat(self):
        self.assertTrue(len(self.TestSeries.all_types) == 1)
        self.assertTrue(self.TestSeries.all_types == ['renewable'])
        self.assertTrue(self.TestSeries.minute_res == 15)

    def test_fill(self):
        self.TestSeries.fill_time_series()

        #Test minimum time
        time_min_exp = fetchInputs.get_datetime_from_str('2016-01-01 00:15:00')
        self.assertTrue(self.TestSeries.time_min == time_min_exp)

        #Test maximum time
        time_max_exp = fetchInputs.get_datetime_from_str('2016-01-01 23:45:00')
        self.assertTrue(self.TestSeries.time_max == time_max_exp)

    def test_negative_recovery(self):

        #Negative value
        key = fetchInputs.get_datetime_from_str('2016-01-01 10:45:00')
        self.assertTrue(self.TestSeries.time_value_map['renewable'][key] == 0)

        #Post negative value
        key = fetchInputs.get_datetime_from_str('2016-01-01 11:00:00')
        self.assertTrue(self.TestSeries.time_value_map['renewable'][key] == 8.25634765625)

        #Negative value
        key = fetchInputs.get_datetime_from_str('2016-01-01 12:30:00')
        self.assertTrue(self.TestSeries.time_value_map['renewable'][key] == 0)

        #Post negative value
        key = fetchInputs.get_datetime_from_str('2016-01-01 12:45:00')
        self.assertTrue(self.TestSeries.time_value_map['renewable'][key] == 9.85595703125)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
