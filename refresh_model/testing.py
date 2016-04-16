import unittest
from worker import *

class TestRefreshModel(unittest.TestCase):
    def test_get_votes(self):
        init_gearman_client()
        votes = get_votes_for_user('iandioch')
        self.assertTrue(len(votes) > 0)
        votes = get_votes_for_user(6969)
        self.assertFalse(len(votes) > 0)

    def test_get_user_data(self):
        init_gearman_client()
        user_data = get_user_data('iandioch')
        self.assertTrue(user_data is not None)
        user_data = get_user_data(1337)
        self.assertTrue(user_data is None)

    def test_update_model(self):
        init_gearman_client()
        user_data = get_user_data('iandioch')
        if 'model' in user_data:
            del user_data['model']

        update_user_data('iandioch', user_data)
        
        user_data = get_user_data('iandioch')
        self.assertFalse('model' in user_data)

        votes = []
        model = build_model(user_data, votes)
        self.assertFalse(model is None)

        user_data['model'] = model
        update_user_data('iandioch', user_data)

        user_data = get_user_data('iandioch')
        self.assertTrue('model' in user_data)

if __name__ == '__main__':
    unittest.main()
