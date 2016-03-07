from scraper import Scraper
from datetime import datetime
import bson
import gearman

#Log some information
def log(level, message):
    levels = ['INFO:','WARNING:','ERROR:']
    time = str(datetime.now()).replace('-','/')[:-7]
    print time,levels[level],message
    pass

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
            "items":1,
            },
        }))
    url_fields_gotten = gm_client.submit_job("db-get", to_get_urls_ids)
    bson_object = bson.BSON.decode(bson.BSON(url_fields_gotten.result))

    return bson_object["docs"]


# updates all of the item fields for all the unique feeds in the feeds db
def update_all_feeds(worker,job):
    log(0,"'update-all-feeds' initiated")
    log(0,"Retrieving data from feed db")
    feed_db_data = get_feed_db_data()

    for doc in feed_db_data:
            log(0,"Loading items in feed: " + doc['url'])
            updated_item_list = []
            result = scr.get_feed_data(doc['url'])#list of item dicts

            for item in result:
                for db_item in doc['items']:
                    if item['link'] == db_item['link']:
                        #If item already in db
                        updated_item_list.append(db_item)
                        break
                else:
                    #Runs if loop doesn't break, implying new item
                    updated_item_list.append({
                        'name':item['name'],
                        'pub_date':item['pub_date'],
                        'link':item['link'],
                        'article_text': '',
                        })


            bson_data = None
            try:
                    bson_data = bsonify_update_data(doc['_id'], doc['url'], updated_item_list)
            except Exception as e:
                    log(2,str(e))
                    return str(bson.BSON.encode({
                        "status":"error",
                        "error-description":str(e)
                        }))

            log(0,"ready to db-update")
            update_response = None
            try:
                    update_response = gm_client.submit_job('db-update', str(bson_data), background=True)
            except Exception as e:
                    log(2,str(e))
                    return str(bson.BSON.encode({
                        "status":"error",
                        "error-description":str(e)
                        }))
            log(0,"update response: " + str(update_response))

            log(0,"Submitting items for scraping")
            #Submit items for scrapin
            text_getter_data = str(bson.BSON.encode({"url" : doc['url']}))
            try:
                    update_response = gm_client.submit_job('article-text-getter',text_getter_data, background=True)
            except Exception as e:
                    log(2,str(e))
                    return str(bson.BSON.encode({
                        "status":"error",
                        "error-description":str(e)
                        }))
            log(0,"article-text-getter update response: " + str(update_response))



    log(0,"'update-all-feeds' finished")
    return str(bson.BSON.encode({
        "status":"ok",
        "updated_feeds":[x['_id'] for x in feed_db_data],
        }))


scr = Scraper()


# make the gearman worker to update feeds or add a new feed(adding not done yet). Make the client to allow adder and getter job calls.
log(0,"Initiating gearman worker")
gm_worker = gearman.GearmanWorker(['localhost:4730'])
log(0,"Initiating gearman client")
gm_client = gearman.GearmanClient(["localhost:4730"])

# register the tasks -> update all the feeds, add new feeds.
log(0,"Registering task 'update-all-feeds'")
gm_worker.register_task('update-all-feeds', update_all_feeds)
gm_worker.work()
