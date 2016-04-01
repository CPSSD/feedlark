import unittest
import all_topics as topics
import bson

class TestScraping(unittest.TestCase):

    def test_mean(self):
        self.assertEqual(topics.mean([]), None)
        self.assertEqual(topics.mean([1]), 1)
        self.assertEqual(topics.mean([1,2]), 1.5)
        self.assertEqual(topics.mean([1,1,1,1,1]), 1)
        self.assertEqual(topics.mean([1,2,3,4,5]), 3)
        self.assertEqual(topics.mean([1.1,2.2,2.3,2.3,4.6,82.9]), 15.9)
        self.assertEqual(topics.mean([-5, -6, 12, -6, -4, 2097]), 348)

    def test_mode(self):
        self.assertEqual(topics.mode([]), None)
        self.assertEqual(topics.mode([1,1,2,2]), None)
        self.assertRaises(ValueError, topics.mode, [5,4,3,2,1]) # function assumes input is order in ascending order
        self.assertRaises(ValueError, topics.mode, [1,2,2,2,2,4,3])
        self.assertEqual(topics.mode([1,1,1,2,2]), 1)
        self.assertEqual(topics.mode([1]), 1)
        self.assertEqual(topics.mode([52,54,56,58]), None)

    def test_median(self):
        self.assertEqual(topics.median([]), None)
        self.assertEqual(topics.median([1]), 1)
        self.assertEqual(topics.median([1,1]), 1)
        self.assertEqual(topics.median([1,2]), 1.5)
        self.assertEqual(topics.median([1,2,3]), 2)
        self.assertEqual(topics.median([1,2,2,3]), 2)
        self.assertEqual(topics.median([1,2,3,4]), 2.5)
        self.assertRaises(ValueError, topics.median, [5,4,3,2,1])
        self.assertRaises(ValueError, topics.median, [1,2,2,2,2,4,3])

if __name__ == '__main__':
    unittest.main()
