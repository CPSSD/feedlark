import unittest
import gearman
import bson
from aggregator import Aggregator#Runs aggregator.py
from kw_score import fast_score, score

class TestAggregation(unittest.TestCase):

    def test_get_users(self):
        gm_client = gearman.GearmanClient(['localhost:4730'])
        agg = Aggregator(gm_client)

        user_data = agg.get_users()
        for i in range(len(user_data)):
            del user_data[i]['_id']

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


    def test_get_feed_items(self):
        gm_client = gearman.GearmanClient(['localhost:4730'])
        agg = Aggregator(gm_client)

        feed_items = agg.get_feed_items('http://spritesmods.com/rss.php')
        expected_response = [
            {
                u"name": u"Creating the Tamagotchi Singularity",
                u"pub_date": u"time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=18, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
                u"link": u"http://spritesmods.com/?art=tamasingularity&amp;f=rss",
                u"article_text": u"Building the Tamagotchi Singularity. The Singularity has happened, but not to us. I also gave a talk about this project on the Hackaday Superconference 2015. There is a video available of that if you'd rather watch me talk. You can also directly view the end result if you so please. As some of you may know, I recently moved from the Netherlands to Shanghai. In the long term, this is great for my hobby: I got a fair amount of stuff out of China anyway, and me moving there meant I wouldn't have to wait a month for it to arrive anymore. In the short term, my ability to build things took somewhat of a hit, though: aside from my oscilloscope and some small bits and bobs I thought I would have a hard time getting in China, I left most of my electronic stuff back in the Netherlands, with the idea that I would be able to buy myself most stuff anew when I had the time."
            }]
        self.assertEqual(feed_items[0], expected_response[0])

    def test_put_g2g(self):
        gm_client = gearman.GearmanClient(['localhost:4730'])
        agg = Aggregator(gm_client)

##        add_request = bson.BSON.encode({
##            'database':'feedlark',
##            'collecion':'g2g',
##            'data':{
##                'username':'__test123__',
##                'test_parameter':'NOLO'
##                }
##            })
##        gm_client.submit_job('db-add',str(add_request))

        test_document = {
            'username':'iandioch',
            'test_parameter':'YOLO',
            }
        agg.put_g2g('iandioch',test_document)

        get_request = bson.BSON.encode({
            'database':'feedlark',
            'collection':'g2g',
            'query':{
                'username':'iandioch',
                },
            'projection':{
                'test_parameter':1,
                },
            })
        g2g_data = gm_client.submit_job('db-get',str(get_request)).result
        self.assertEqual(bson.BSON(g2g_data).decode()['docs'][0]['test_parameter'], 'YOLO')

    def test_fast_score(self):
        u_words = {'pancakes':3,'syrup':12, 'communism':-10}

        a_words = {'communism':0.2,'syrup':0.1}
        sticky_marxism = fast_score(a_words, u_words)

        a_words2 = {'pancakes':0.2,'syrup':0.1}
        trip_to_canada = fast_score(a_words2, u_words)
        
        self.assertTrue(sticky_marxism < trip_to_canada)

    def test_score(self):
        u_words = {'pancakes':3,'syrup':12, 'communism':-10}

        a_words = {'communism':0.2,'syrup':0.1}
        sticky_marxism = score(a_words, u_words)

        a_words2 = {'pancakes':0.2,'syrup':0.1}
        trip_to_canada = score(a_words2, u_words)

        self.assertTrue(sticky_marxism < trip_to_canada)


        a_words = {'marxism':0.2,'sugar':0.1}
        sticky_marxism = score(a_words, u_words)

        a_words2 = {'cake':0.2,'honey':0.1}
        trip_to_canada = score(a_words2, u_words)

        self.assertTrue(sticky_marxism < trip_to_canada)


if __name__ == '__main__':
    unittest.main()
