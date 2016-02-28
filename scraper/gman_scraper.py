from scraper import Scraper
import bson
import gearman

# convert given data to bson in valid format for db-update
def bsonify_update_data(item_id, url , allData):
    items_list = {
        "database":"feedlark",
        "collection":"feed",
        "data":{
            "updates":{
                "items":allData,
                "url":url
                },
            "selector":{
                "_id": item_id
                },
            },
        }
    return bson.BSON.encode(items_list)

# submits a job to 'db-get' to get all ids and urls of the feeds
def get_feed_db_data():
	# format the request
	to_get_urls_ids = str(bson.BSON.encode({
            "database":"feedlark",
            "collection":"feed",
            "query": {},
            "projection":{
                "_id":1,
                "url":1,
                "items":[{
                    "link":1,
                    "pub_date":1,
                    "link":1,
                    "article_text":1,
                    }],
                },
            }))
	url_fields_gotten = gm_client.submit_job("db-get", to_get_urls_ids)
	bson_object = bson.BSON.decode(bson.BSON(url_fields_gotten.result))
	print "response: " + str(bson_object)
	
	return bson_object["docs"]


# updates all of the item fields for all the unique feeds in the feeds db
def update_all_feeds(worker,job):
	print "'update-all-feeds' initiated"
	print "Retrieving data from feed db"
	feed_db_data = get_feed_db_data()

	for doc in feed_db_data:
		print "Loading items in feed: " + doc['url']
		updated_item_list = []
		result = scr.get_feed_data(doc['url'])#list of item dicts

		items_to_scrape = []
		for item in result:
                    for db_item in doc['items']:
                        if item['link'] == db_item['link']:
                            #If item already in db
                            updated_item_list.append(db_item)
                            break
                    else:
                        #Runs if loop doesn't break, implying new item
                        items_to_scrape.append({
                            '_id':doc['_id'],
                            'link':item['link'],
                            })
                        updated_item_list.append({
                            'name':item['name'],
                            'pub_date':item['pub_date'],
                            'link':item['link'],
                            })
    
                    
		bson_data = None
		try:
			bson_data = bsonify_update_data(doc['_id'], doc['url'], updated_item_list)
		except Exception as e:
			print e
			return str(bson.BSON.encode({
                            "status":"error",
                            "error-description":str(e)
                            }))
		
		print "ready to db-update"
		update_response = None
		try:
			update_response = gm_client.submit_job('db-update', str(bson_data), background=True)
		except Exception as e:
			print e
			return str(bson.BSON.encode({
                            "status":"error",
                            "error-description":str(e)
                            }))
                print "update response: " + str(update_response)

                print "Submitting items for scraping"
		#Submit items for scraping
		for item in items_to_scrape:                
                    text_getter_data = str(bson.BSON.encode(item))
                    gm_client.submit_job('article-text-getter',text_getter_data, background=True)
                
		

	print "'update-all-feeds' finished"
	return str(bson.BSON.encode({
            "status":"ok",
            "updated_feeds":[x['_id'] for x in feed_db_data],
            }))


scr = Scraper()


# make the gearman worker to update feeds or add a new feed(adding not done yet). Make the client to allow adder and getter job calls.
print "Initiating gearman worker"
gm_worker = gearman.GearmanWorker(['localhost:4730'])
print "Initiating Client"
gm_client = gearman.GearmanClient(["localhost:4730"])

# register the tasks -> update all the feeds, add new feeds.
print "Registering task 'update-all-feeds'"
gm_worker.register_task('update-all-feeds', update_all_feeds)
gm_worker.work()
