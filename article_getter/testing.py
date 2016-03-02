import unittest
from article_text_getter import Article_getter
import gearman
import bson

class TestScraping(unittest.TestCase):

    def test_article_getter(self):
        testing = Article_getter()
        try:
            f = open("test_article_text_data.txt","r")
            text = f.read()
            f.close()
        except:
            print "file not found"
        test_text = testing.get_article_text("http://u.m1cr0man.com/l/feed.xml")
        self.assertEqual(text, test_text + "\n")

if __name__ == '__main__':
    unittest.main()
