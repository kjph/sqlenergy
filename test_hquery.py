import unittest
from hquery import *

# class GetQueryBetweenDatesTest(unittest.TestCase):

#     def test_correct_one(self):
#         r = get_query_between_dates('table', '2015-10-11', '2016-10-11')
#         self.assertTrue(r == "select VALUE AS KWH, FROM_UNIXTIME(TIMESTAMP/1000) AS timestamp_good FROM table where ((TIMESTAMP/1000) > UNIX_TIMESTAMP('2015-10-11')) AND ((TIMESTAMP/1000) < UNIX_TIMESTAMP('2016-10-11'))")

class LoadTableListTest(unittest.TestCase):

    def test_correct_load(self):
        r = load_table_list('res/table_list.txt')
        self.assertTrue(len(r) == 12)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
