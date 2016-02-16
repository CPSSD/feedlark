from scraper import Scraper
import json
import gearman


def addNewFeed(allData):
	items_list = {"database":"feeds","collection":"rss", "data": allData}
	return json.dumps(items_list)


scr = Scraper()
gm_client = gearman.GearmanClient(["localhost:4730"])

json_data = addNewFeed(scr.get_feed_data("http://spritesmods.com/rss.php"))

gm_client.submit_job("db-add", json_data)



#for item in scr.get_feed_data("http://spritesmods.com/rss.php"):
#    print item
#    print
