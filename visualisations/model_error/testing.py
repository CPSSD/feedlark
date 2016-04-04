import gearman
import bson
import unittest
import model_error as me

class TestDbTools(unittest.TestCase):
    def test_get_username(self):
        self.assertEqual(me.get_username_from_input(['', 'jeremy']), 'jeremy')
        self.assertEqual(me.get_username_from_input(['', 'jeremy', 'corbyn']), 'jeremy corbyn')

if __name__ == '__main__':
    unittest.main()
