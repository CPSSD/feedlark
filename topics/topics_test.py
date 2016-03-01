import unittest
from topics import get_topics

class TestTopics(unittest.TestCase):
    def test_topics_without_stop_words(self):
        article = "banana banana banana"
        topics = get_topics(article)
        self.assertEquals(len(topics), 1)
        self.assertEquals(topics[0], "banana")

    def test_topics_with_stop_words(self):
        article = "banana banana banana the"
        topics = get_topics(article)
        self.assertEquals(len(topics), 1)
        self.assertEquals(topics[0], "banana")
        self.assertFalse("the" in topics)

    def test_multiple_topics_without_stop_words(self):
        article = "banana banana banana orange orange"
        topics = get_topics(article)
        self.assertEquals(len(topics), 2)
        self.assertTrue("banana" in topics)
        self.assertTrue("orange" in topics)

    def test_multiple_topics_with_stop_words(self):
        article = "the banana a banana an banana or orange and orange"
        topics = get_topics(article)
        self.assertEquals(len(topics), 2)
        self.assertTrue("banana" in topics)
        self.assertTrue("orange" in topics)
        self.assertFalse("the" in topics)
