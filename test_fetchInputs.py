import unittest
from fetchInputs import *

class DatabaseInputsTest(unittest.TestCase):

    def TestIncorrectType(self):
        self.assertTrue(database_inputs('hello.j') == -1)
