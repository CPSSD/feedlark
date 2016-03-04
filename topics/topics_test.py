import unittest
from topics import get_topics

class TestTopics(unittest.TestCase):
    def test_topics_without_stop_words(self):
        article = u"banana banana banana"
        topics = get_topics(article)
        self.assertEqual(len(topics), 1)
        self.assertTrue("banana" in topics)

    def test_topics_with_stop_words(self):
        article = u"banana banana banana the"
        topics = get_topics(article)
        self.assertEqual(len(topics), 1)
        self.assertTrue("banana" in topics)
        self.assertFalse("the" in topics)

    def test_multiple_topics_without_stop_words(self):
        article = u"banana banana banana orange orange"
        topics = get_topics(article)
        self.assertEqual(len(topics), 2)
        self.assertTrue("banana" in topics)
        self.assertTrue("orange" in topics)

    def test_multiple_topics_with_stop_words(self):
        article = u"the banana a banana an banana or orange and orange"
        topics = get_topics(article)
        self.assertEqual(len(topics), 2)
        self.assertTrue("banana" in topics)
        self.assertTrue("orange" in topics)
        self.assertFalse("the" in topics)

    def test_top_values_of_dict(self):
        d = {'cat':7, 'dog':4, 'gerbil': 5, 'watermelon':1}
        e = limit_dict(d, 3)
        self.assertEqual(len(e), 3)
        self.assertTrue('cat' in e)
        self.assertTrue('dog' in e)
        self.assertTrue('gerbil' in e)
        self.assertFalse('watermelon' in e)

if __name__ == '__main__':
    unittest.main()
