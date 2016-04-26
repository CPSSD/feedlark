import unittest
from updater import *

class TestOpinionUpdater(unittest.TestCase):
    def test_update_topic_counts_positive(self):
        prev_topics = {"banana":3, "split":-17}
        changes = ["banana", "pie"]
        new_topics = update_topic_counts(prev_topics, changes, True)
        self.assertTrue("pie" in new_topics and "banana" in new_topics and "split" in new_topics)
        self.assertEqual(new_topics["pie"], 1)
        self.assertEqual(new_topics["banana"], 4)
        self.assertEqual(new_topics["split"], -17)

    def test_update_topic_counts_negative(self):
        prev_topics = {"banana":3, "split":-17}
        changes = ["banana", "pie"]
        new_topics = update_topic_counts(prev_topics, changes, False)
        self.assertTrue("pie" in new_topics and "banana" in new_topics and "split" in new_topics)
        self.assertEqual(new_topics["pie"], -1)
        self.assertEqual(new_topics["banana"], 2)
        self.assertEqual(new_topics["split"], -17)

    def test_get_user_data(self):
        init_gearman_client()
        data = get_user_data('sully')
        self.assertFalse(data is None)
        data = get_user_data(1337) # should be no results for non-string usernames
        self.assertTrue(data is None)

    def test_get_feed_data(self):
        init_gearman_client()
        data = get_feed_data('https://news.ycombinator.com/rss')
        self.assertFalse(data is None)
        data = get_feed_data('ftp://example.ml/feed.yaml')
        self.assertTrue(data is None)        

    def test_vote_already_exists(self):
        init_gearman_client()
        exists = vote_already_exists('iandioch', 'http://www.apple.com/customer-letter/')
        self.assertTrue(exists)
        exists = vote_already_exists('iandioch', 'ftp://communism.example/syrup')
        self.assertFalse(exists)
        exists = vote_already_exists('sully', 'http://www.apple.com/customer-letter/')
        self.assertFalse(exists)
        exists = vote_already_exists('sully', 'http://spritesmods.com/?art=tamasingularity&amp;f=rss')
        self.assertTrue(exists)

if __name__ == '__main__':
    unittest.main()
