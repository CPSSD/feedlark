from article_text_getter import Article_getter
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
    #print "response: " + str(bson_object)

    return bson_object["docs"]

# updates all of the item fields for all the unique feeds in the feeds db
def update_article_text():#worker,job):
    print "'update-all-article-text' initiated"
    print "Retrieving data from feed db"
    feed_db_data = get_feed_db_data()

    for doc in feed_db_data:
        print "Loading items in feed: " + doc['url'] + " for article getter"
        updated_item_list = []

        for db_item in doc['items']:
            if db_item['article_text'] != "":
                print "2"
                #If item in db already has article_text
                updated_item_list.append(db_item)
                continue
            else:
                print "3"
                #Runs if loop doesn't break, implying new item
                updated_item_list.append({
                    'name':db_item['name'],
                    'pub_date':db_item['pub_date'],
                    'link':db_item['link'],
                    'article_text': art_get.get_article_text(db_item['link'])
                })
                print "4"

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
    print "'update-all-article-text' finished"
    return str(bson.BSON.encode({
            "status":"ok",
            "updated_feeds":[x['_id'] for x in feed_db_data],
            }))

art_get = Article_getter()

# make the gearman worker to update feeds or add a new feed(adding not done yet). Make the client to allow adder and getter job calls.
print "Initiating gearman worker"
gm_worker = gearman.GearmanWorker(['localhost:4730'])
print "Initiating Client"
gm_client = gearman.GearmanClient(["localhost:4730"])

# register the tasks -> update all the article text for all feeds.
print "Registering task 'update-all-article-text'"
gm_worker.register_task('update-all-article-text', update_article_text)
update_article_text()
#gm_worker.work()
