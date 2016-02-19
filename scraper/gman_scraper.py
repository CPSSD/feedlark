from scraper import Scraper
import bson
import gearman

# convert given data to bson in valid format for db-update
def bsonify_update_data(item_id, url , allData):
    items_list = {"database":"feedlark","collection":"feed", "data": {"updates" : {"items":allData}, "selector": {"_id": item_id } } }
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
		urls.append(str(item['url']))
		ids.append(item['_id'])

	return urls, ids


# updates all of the item fields for all the unique feeds in the feeds db
def update_all_feeds(worker,job):
	print "Update feed Worker initiated"
	feed_urls, feed_ids = get_all_feed_ids_url()
	print "Retrieving data from feed db"
	test_holder = []
	for i in range(len(feed_urls)):
		print feed_urls[i]
                result = scr.get_feed_data(feed_urls[i]) # returns a list of dictionaries, a dict for each item in the feed
                print feed_urls[i] + " get!"
                #print result 
                bson_data = None
                try:
                    bson_data = bsonify_update_data(feed_ids[i], None, result)
                except Exception as e:
                    print e
                #print "db-update arg: " + str(bson_data)
                print "ready to db-update"
                update_response = None
                try:
                    update_response = gm_client.submit_job('db-update', str(bson_data))
                except Exception as e:
                    print e
                print "update response: " + update_response
                #print result
		#bson_data = bsonify_update_data(item_ids[i], item_urls[i], scr.get_feed_data(item_urls[i]))
                #print bson_data
                test_holder.append(result)
		#test_holder.append(bson_data)
		#gm_client.submit_job("db-update", bson_data)
	print "Worker Done"
        #print test_holder
        return str(bson.BSON.encode({"results":test_holder}))


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
