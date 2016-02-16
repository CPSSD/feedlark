from scraper import Scraper
import json
import gearman

# Parses data to json to allow for db update
def parse_to_json(id, url , allData):
	items_list = {"database":"feedlark","collection":"feeds", "data": {updates : {"items":allData}, "id": id } }
	return json.dumps(items_list)

# parses data to json to allow for adding to db
def parse_to_json(url , allData):
	items_list = {"database":"feedlark","collection":"feeds", "data": {"url":url, "items":allData}}
	return json.dumps(items_list)

# submits a job to getter gearman worker to get all ids and urls (references) of the feeds
def get_all_feed_ids_url():
	to_get = {"database":"feedlark","collection":"feeds", "query": {}}
	fields_gotten = gm_client.submit_job("db-get", json.dumps(json_to_get))
	return fields_gotten

# updates all of the item fields for all the unique feeds in the feeds db
def update_all_feeds():
	feed_references = get_all_feed_ids_url()
	for i in range(len(feed_references)):
		json_data = parse_to_json(feed_references["id"], feed_references["url"], scr.get_feed_data(url))
		print json_data
		gm_client.submit_job("db-update", json_data)

# Adds a new feed to the feeds db
def add_feed(url):
	json_data = parse_to_json(url, scr.get_feed_data(url))
	print json_data
	completed_job_request = gm_client.submit_job("db-add", json_data)
	check_request_status(completed_job_request)

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.unique

scr = Scraper()
gm_client = gearman.GearmanClient(["localhost:4730"])

#add_feed("http://spritesmods.com/rss.php")
