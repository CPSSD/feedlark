import unittest
import gearman
import bson
from random import random
from aggregator import Aggregator  # Runs aggregator.py
from kw_score import fast_score, score
from predict import Classification


class TestAggregation(unittest.TestCase):

    def test_get_users(self):
        gm_client = gearman.GearmanClient(['localhost:4730'])
        agg = Aggregator(gm_client)

        user_data = agg.get_users()
        for i in range(len(user_data)):
            del user_data[i]['_id']
            if 'words' in user_data[i]:
                del user_data[i]['words']

        expected_response = [
            {
                u'username': u'iandioch',
                u'subscribed_feeds': [
                    u'https://news.ycombinator.com/rss'
                    ],
            },
            {
                u'username': u'sully',
                u'subscribed_feeds': [
                    u'https://news.ycombinator.com/rss',
                    u'http://spritesmods.com/rss.php',
                    u'http://dave.cheney.net/feed'
                    ],
            },
            {
                u'username': u'theotherguys',
                u'subscribed_feeds': [
                    u'https://news.ycombinator.com/rss',
                    u'http://spritesmods.com/rss.php'
                    ],
            }]

        self.assertEqual(user_data, expected_response)

    def test_put_g2g(self):
        gm_client = gearman.GearmanClient(['localhost:4730'])
        agg = Aggregator(gm_client)

#        add_request = bson.BSON.encode({
#            'database':'feedlark',
#            'collecion':'g2g',
#            'data':{
#                'username':'__test123__',
#                'test_parameter':'NOLO'
#                }
#            })
#        gm_client.submit_job('db-add',str(add_request))

        test_document = {
            'username': 'iandioch',
            'test_parameter': 'YOLO',
            }
        agg.put_g2g('iandioch', test_document)

        get_request = bson.BSON.encode({
            'database': 'feedlark',
            'collection': 'g2g',
            'query': {
                'username': 'iandioch',
                },
            'projection': {
                'test_parameter': 1,
                },
            })
        g2g_data = gm_client.submit_job('db-get', str(get_request)).result
        self.assertEqual(
            bson.BSON(g2g_data).decode()['docs'][0]['test_parameter'], 'YOLO')

    def test_fast_score(self):
        u_words = {'pancakes': 3, 'syrup': 12, 'communism': -10}

        a_words = {'communism': 0.2, 'syrup': 0.1}
        sticky_marxism = fast_score(a_words, u_words)

        a_words2 = {'pancakes': 0.2, 'syrup': 0.1}
        trip_to_canada = fast_score(a_words2, u_words)

        self.assertTrue(sticky_marxism < trip_to_canada)

    def test_score(self):
        u_words = {'pancakes': 3, 'syrup': 12, 'communism': -10}

        a_words = {'communism': 0.2, 'syrup': 0.1}
        sticky_marxism = score(a_words, u_words)

        a_words2 = {'pancakes': 0.2, 'syrup': 0.1}
        trip_to_canada = score(a_words2, u_words)

        self.assertTrue(sticky_marxism < trip_to_canada)

        a_words = {'marxism': 0.2, 'sugar': 0.1}
        sticky_marxism = score(a_words, u_words)

        a_words2 = {'cake': 0.2, 'honey': 0.1}
        trip_to_canada = score(a_words2, u_words)

        self.assertTrue(sticky_marxism < trip_to_canada)

    def test_classification(self):
        c = Classification()
        x = []
        y = []
        print 'Training test model'
        for i in xrange(1000):
            x.append([random()*3, random()*5, -random()])
            y.append(1)
        for i in xrange(1000):
            x.append([random()*5 + 2, random()*3 - 1.5, random()])
            y.append(-1)
        c.train(x, y)
        p = c.predict([[2.1, 3.1, -0.30]])

        #self.assertTrue(p[0] > 0.5)

        q = c.predict([[5.2, -0.5, 0.7]])
        
        self.assertTrue(q[0] < 0.5)


if __name__ == '__main__':
    unittest.main()
