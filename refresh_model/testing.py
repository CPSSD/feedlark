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

    def test_update_model(self):
        print 'Testing refresh-model build_model'
        init_gearman_client()
        user_data = get_user_data('iandioch')
        if 'model' in user_data:
            del user_data['model']

        update_user_data('iandioch', user_data)
        
        user_data = get_user_data('iandioch')
        self.assertFalse('model' in user_data)

        print 'Building empty model'
        votes = []
        model = build_model(user_data, votes)
        self.assertTrue(model is None)

        print 'Building populated model'
        votes = [{
            'username': 'iandioch',
            'article_url': 'http://www.apple.com/customer-letter/',
            'feed_url': 'https://news.ycombinator.com/rss',
            'positive_opinion': False,
            'vote_datetime': datetime.now()
        }]
        model = build_model(user_data, votes)
        self.assertFalse(model is None)

if __name__ == '__main__':
    unittest.main()
