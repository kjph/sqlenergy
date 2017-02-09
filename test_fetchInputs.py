import unittest
from fetchInputs import *

class TypeTableMapTest(unittest.TestCase):

    def type_table_map_len(self):
        r = load_table_list('res/test_table_list.txt')
        self.assertTrue(len(r) == 1)

    def type_table_map_value(self):
        r = load_table_list('res/test_table_list.txt')
        self.assertTrue(r['renewable'] == ['emsj01_01_pv_pb_eastwestrealenergy'])

def main():
    unittest.main()

if __name__ == '__main__':
    main()
