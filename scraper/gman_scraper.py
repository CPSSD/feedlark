from scraper import Scraper
import bson
import gearman

# convert given data to bson in valid format for db-update
def bsonify_update_data(item_id, url , allData):
    items_list = {"database":"feedlark","collection":"feed", "data": {"updates" : {"items":allData, "url":url}, "selector": {"_id": item_id } } }
    return (bson.BSON.encode(items_list))

# submits a job to getter gearman worker to get all ids and urls (references) of the feeds
def get_all_feed_ids_url():
	# fotmat the requests from the db
	to_get_urls_ids = str(bson.BSON.encode({"database":"feedlark","collection":"feed", "query": {},"projection":{"_id":1, "url":1}}))
	# submit the jobs to get the ids and urls from the db.

        print "db-get data: " + to_get_urls_ids

	url_fields_gotten = gm_client.submit_job("db-get", to_get_urls_ids)
	bson_object = bson.BSON.decode(bson.BSON(url_fields_gotten.result))
        print "response: " + str(bson_object)
	#extract the url and id strings
	urls = []
	ids = []
	for item in bson_object["docs"]:
                if "url" not in item or "_id" not in item:
                    continue
		urls.append(str(item['url']))
		ids.append(item['_id'])

	return urls, ids


# updates all of the item fields for all the unique feeds in the feeds db
def update_all_feeds(worker,job):
	print "'update-all-feeds' initiated"
	feed_urls, feed_ids = get_all_feed_ids_url()
        print feed_urls
	print "Retrieving data from feed db"
	test_holder = []
	for i in range(len(feed_urls)):
		print "Loading items in feed " + str(feed_urls[i])
                result = scr.get_feed_data(feed_urls[i]) # returns a list of dictionaries, a dict for each item in the feed
                bson_data = None
                try:
                    bson_data = bsonify_update_data(feed_ids[i], feed_urls[i], result)
                except Exception as e:
                    print e
                    raise
                print "ready to db-update"
                update_response = None
                try:
                    update_response = gm_client.submit_job('db-update', str(bson_data), background=True)
                except Exception as e:
                    print e
                    raise
                print "update response: " + str(update_response)
                test_holder.append(result)
	print "'update-all-feeds' finished"
        return str(bson.BSON.encode({"updated_feeds":feed_ids}))


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
