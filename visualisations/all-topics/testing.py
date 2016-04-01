import unittest
import all_topics as topics
import bson

class TestScraping(unittest.TestCase):

    def test_mean(self):
        self.assertEqual(topics.mean([]), None)
        self.assertEqual(topics.mean([1,1,1,1,1]), 1)
        self.assertEqual(topics.mean([1,2,3,4,5]), 3)
        self.assertEqual(topics.mean([1.1,2.2,2.3,2.3,4.6,82.9]), 15.9)
        self.assertEqual(topics.mean([-5, -6, 12, -6, -4, 2097]), 348)

if __name__ == '__main__':
    unittest.main()
