import unittest
from updater import update_topic_counts, get_user_data, init_gearman_client

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

if __name__ == '__main__':
    unittest.main()
