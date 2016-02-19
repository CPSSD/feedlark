import unittest
import gearman
import bson
from aggregator import Aggregator#Runs aggregator.py

class TestAggregation(unittest.TestCase):

    def test_get_users(self):
        gm_client = gearman.GearmanClient(['localhost:4730'])
        agg = Aggregator(gm_client)
        
        user_data = agg.get_users()
        expected_response = [
            {
                u'username': u'iandioch',
                u'subscribed_feeds': [
                    u'https://news.ycombinator.com/rss'
                    ],
                u'_id': bson.objectid.ObjectId('56c78d5a36f379aecc477bbd')
            },
            {
                u'username': u'sully',
                u'subscribed_feeds': [
                    u'https://news.ycombinator.com/rss',
                    u'http://spritesmods.com/rss.php',
                    u'http://dave.cheney.net/feed'
                    ],
                u'_id': bson.objectid.ObjectId('56c78d5a36f379aecc477bbe')
            },
            {
                u'username': u'theotherguys',
                u'subscribed_feeds': [
                    u'https://news.ycombinator.com/rss',
                    u'http://spritesmods.com/rss.php'
                    ],
                u'_id': bson.objectid.ObjectId('56c78d5a36f379aecc477bbf')
            }]

        self.assertEqual(user_data, expected_response)


if __name__ == '__main__':
    unittest.main()
