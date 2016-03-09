import unittest
from topics import get_topics, limit_dict, update_article_data

class TestTopics(unittest.TestCase):
    def test_topics_without_stop_words(self):
        article = u"banana banana banana"
        topics = get_topics(article)
        self.assertEqual(len(topics), 1)
        self.assertTrue("banana" in topics)

    def test_topics_with_stop_words(self):
        article = u"banana banana banana the"
        topics = get_topics(article)
        self.assertEqual(len(topics), 1)
        self.assertTrue("banana" in topics)
        self.assertFalse("the" in topics)

    def test_multiple_topics_without_stop_words(self):
        article = u"banana banana banana orange orange"
        topics = get_topics(article)
        self.assertEqual(len(topics), 2)
        self.assertTrue("banana" in topics)
        self.assertTrue("orange" in topics)

    def test_multiple_topics_with_stop_words(self):
        article = u"the banana a banana an banana or orange and orange"
        topics = get_topics(article)
        self.assertEqual(len(topics), 2)
        self.assertTrue("banana" in topics)
        self.assertTrue("orange" in topics)
        self.assertFalse("the" in topics)

    def test_top_values_of_dict(self):
        d = {'cat':7, 'dog':4, 'gerbil': 5, 'watermelon':1}
        e = limit_dict(d, 3)
        self.assertEqual(len(e), 3)
        self.assertTrue('cat' in e)
        self.assertTrue('dog' in e)
        self.assertTrue('gerbil' in e)
        self.assertFalse('watermelon' in e)

    def test_punctuation(self):
        article = u"the cat was on the mat."
        topics = get_topics(article)
        self.assertEqual(len(topics), 2)
        self.assertTrue("cat" in topics)
        self.assertTrue("mat" in topics)
        self.assertFalse("." in topics)

    def test_adding_data_to_db_entry(self):
        old_data = {"url": "https://news.ycombinator.com/rss", "items": [{"name": "A Message to Our Customers","pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)", "link": "http://www.apple.com/customer-letter/","arictle_text": "February 16, 2016 A Message to Our Customers. The United States government has demanded that Apple take an unprecedented step which threatens the security of our customers. We oppose this order, which has implications far beyond the legal case at hand. This moment calls for public discussion, and we want our customers and people around the country to understand what is at stake."},{"name": "How to get hired at a startup when you don't know anyone","pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)","link": "http://shane.engineer/blog/how-to-get-hired-at-a-startup-when-you-don-t-know-anyone","article_text": "If you really want to be at a company you can do so much better than a resume. A few years ago I saw an early stage startup that I knew I had to be a part of. The only problem was that it was 900 miles away and I had no connection to them. The startup was Formlabs. At they time they had 10 employees, and like most startups reduced risk by hiring people they knew. They were also situated equidistant between MIT and Harvard so there was healthy local competition. The standard approach of sending in my resume and a carefully crafted cover letter didn't work, so I decided to do something dramatic."}]}
        link = "http://shane.engineer/blog/how-to-get-hired-at-a-startup-when-you-don-t-know-anyone"
        modification = {"topics":{"lorem":0.5, "ipsum":0.25, "dolor":0.25}}
        new_data = update_article_data(old_data, link, modification)
        self.assertTrue(len(new_data["items"]), 2)
        self.assertTrue("topics" in new_data["items"][0] or "topics" in new_data["items"][1])
        self.assertFalse("topics" in new_data["items"][0] and "topics" in new_data["items"][1])
	index = 0
        if "topics" in new_data["items"][1]:
            index = 1
        self.assertEqual(new_data["items"][index]["link"], link)
        self.assertTrue("name" in new_data["items"][index])
        self.assertTrue("pub_date" in new_data["items"][index])
        self.assertTrue("article_text" in new_data["items"][index])
        self.assertTrue("topics" in new_data["items"][index])
        self.assertTrue("link" in new_data["items"][index])
        self.assertFalse("topics" in new_data["items"][(index+1)%2])
	

if __name__ == '__main__':
    unittest.main()
