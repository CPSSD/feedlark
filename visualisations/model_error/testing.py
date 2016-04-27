import gearman
import bson
import unittest
import model_error as me

class TestDbTools(unittest.TestCase):
    def test_get_username(self):
        self.assertEqual(me.get_username_from_input(['', 'jeremy']), 'jeremy')
        self.assertEqual(me.get_username_from_input(['', 'jeremy', 'corbyn']), 'jeremy corbyn')
    
    def test_has_enough_classes(self):
        data = [[0, 1], [0, 1], [0, 1]]
        self.assertFalse(me.has_enough_classes(data))
        data.append([0, -1])
        self.assertTrue(me.has_enough_classes(data))
    
    def test_get_model_score(self):
        training = [[[1, -1], 1], [[-1, 1], -1]]
        validation = [[[1, -1], 1]]

        self.assertTrue(me.get_model_score(training, validation) > 0.5)

if __name__ == '__main__':
    unittest.main()
