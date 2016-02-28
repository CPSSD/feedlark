import unittest
from datetime import datetime
from scraper import Scraper
from article_text_getter import Text_scraper
import gearman
import bson

class TestScraping(unittest.TestCase):

    def test_get_feed_data(self):
        scr = Scraper()

        #The url is to a static RSS feed stolen from Hacker News
        test_feed = scr.get_feed_data('http://u.m1cr0man.com/l/feed.xml')

        title = 'Why it is NOT WISE to discuss personal information in front of smart TVs'
        self.assertEqual(test_feed[0]['name'],title)

        link = 'http://www.hackernews.org/2016/02/14/why-it-is-not-wise-to-discuss-personal-information-in-front-of-smart-tvs/'
        self.assertEqual(test_feed[0]['link'],link)

        pub_date = datetime(2016,2,14,21,10,2)
        self.assertEqual(test_feed[0]['pub_date'],pub_date)

        with self.assertRaises(TypeError):
            scr.get_feed_data(666)

    def test_article_getter(self):
        testing = Text_scraper()
        try:
            f = open("test_article_text_data.txt","r")
            text = f.read()
            f.close()
        except:
            print "file not found"
        test_text = testing.get_article_text("http://u.m1cr0man.com/l/feed.xml")
        self.assertEqual(text, test_text)

    """def test_update_all(self):
        # takes too long to do every build
        gearman_client = gearman.GearmanClient(['localhost:4730'])
        raw_result = gearman_client.submit_job('update-all-feeds', '')
        result = bson.BSON.decode(bson.BSON(raw_result))
        self.assertTrue("status" in result)
        self.assertEqual(result["status"], "ok")"""

if __name__ == '__main__':
    unittest.main()
