import unittest
from scraper import Scraper

class TestScraping(unittest.TestCase):

    def test_get_feed_data(self):
        scr = Scraper()

        #The url is to a static RSS feed stolen from Hacker News
        test_feed = scr.get_feed_data('http://u.m1cr0man.com/l/feed.txt')["data"]

        title = 'Why it is NOT WISE to discuss personal information in front of smart TVs'
        self.assertEqual(test_feed[0]['title'],title)

        link = 'http://www.hackernews.org/2016/02/14/why-it-is-not-wise-to-discuss-personal-information-in-front-of-smart-tvs/'
        self.assertEqual(test_feed[0]['link'],link)

        pub_date = 'time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)'
        self.assertEqual(str(test_feed[0]['pub_date']),pub_date)

        with self.assertRaises(TypeError):
            scr.get_feed_data(666)

if __name__ == '__main__':
    unittest.main()
