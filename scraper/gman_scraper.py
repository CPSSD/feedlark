from scraper import Scraper
import json
import gearman

# Parses data to json to allow for db update
def parse_updates_to_json(item_id, url , allData):
	items_list = {"database":"feedlark","collection":"feeds", "data": {"updates" : {"items":allData}, "id": item_id } }
	return json.dumps(items_list)

# parses data to json to allow for adding to db
def parse_to_json(url , allData):
	items_list = {"database":"feedlark","collection":"feeds", "data": {"url":url, "items":allData}}
	return json.dumps(items_list)

# submits a job to getter gearman worker to get all ids and urls (references) of the feeds
def get_all_feed_ids_url():
	# fotmat the requests from the db
	to_get_urls_ids = {"database":"feedlark","collection":"feed", "query": {},"projection":{"_id":1, "url":1}}
	# submit the jobs to get the ids and urls from the db.
	url_fields_gotten = gm_client.submit_job("db-get", json.dumps(to_get_urls_ids))
	
	#extract the url and id strings
	urls = []
	ids = []
	for item in url_fields_gotten.result[9:-2].split(","):
		if "url" in item:
			urls.append(item[11:-1])
		else:
			ids.append(item[9:-1])
	print urls,ids
	return urls, ids


# updates all of the item fields for all the unique feeds in the feeds db
def update_all_feeds(worker,job):
	print "Update feeds Worker initiated"
	item_urls, item_ids = get_all_feed_ids_url()

	test_holder = []
	for i in range(len(item_urls)):
		json_data = parse_updates_to_json(item_ids[i], item_urls[i], scr.get_feed_data(item_urls[i]))
		test_holder.append(json_data)
		#gm_client.submit_job("db-update", json_data)
	print "Worker Done"
	return json.dumps(test_holder)

# Adds a new feed to the feeds db
def add_feed(url):
	json_data = parse_to_json(url, scr.get_feed_data(url))
	print json_data
	#gm_client.submit_job("db-add", json_data)


scr = Scraper()


# make the gearman worker to update feeds or add a new feed(adding not done yet). Make the client to allow adder and getter job calls.
print "Initiating gearman worker"
gm_worker = gearman.GearmanWorker(['localhost:4730'])
print "Initiating Client"
gm_client = gearman.GearmanClient(["localhost:4730"])

# register the tasks -> update all the feeds, add new feeds.
print "Registering task 'update-all-feeds'"
gm_worker.register_task('update-all-feeds', update_all_feeds)
#gm_worker.register_task('add-new-feed', feed_url_to_add)
gm_worker.work()
