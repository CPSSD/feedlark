import unittest
from worker import *
from datetime import datetime

class TestRefreshModel(unittest.TestCase):
    def test_get_votes(self):
        print 'Testing refresh-model get_votes_for_user()'
        init_gearman_client()
        votes = get_votes_for_user('iandioch')
        self.assertTrue(len(votes) > 0)
        votes = get_votes_for_user(6969)
        self.assertFalse(len(votes) > 0)

    def test_get_user_data(self):
        print 'Testing refresh-model get_user_data'
        init_gearman_client()
        user_data = get_user_data('iandioch')
        self.assertTrue(user_data is not None)
        user_data = get_user_data(1337)
        self.assertTrue(user_data is None)

if __name__ == '__main__':
    unittest.main()
