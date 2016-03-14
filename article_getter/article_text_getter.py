import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import bson
import gearman

# Ensure the class is used with a recent Python 2.
assert (2, 5) <= sys.version_info <= (3, 0)


def get_article_text(article_url):
    if type(article_url) != str and type(article_url) != unicode:
        raise TypeError('URL must be a string')
        return 'URL must be a string'

    html = requests.get(article_url).content
    soup = BeautifulSoup(html, 'html.parser')

    for s in soup(['style', 'script', '[document]', 'head', 'title']):
        s.extract()

    return soup.getText().strip().encode("utf-8")

# Log some information


def log(level, message):
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    time = str(datetime.now()).replace('-', '/')[:-7]
    print time, levels[level], message
    pass

# convert given data to bson in valid format for db-update


def bsonify_update_data(item_id, url, all_data):
    items_list = {
        "database": "feedlark",
        "collection": "feed",
        "data": {
            "updates": {
                "items": all_data,
                "url": url
            },
            "selector": {
                "_id": item_id
            },
        },
    }
    return bson.BSON.encode(items_list)

# submits a job to 'db-get' to get all ids and urls of the singular feed


def get_single_feed_db_data(url):
    # format the request
    to_get_urls_ids = str(bson.BSON.encode({
        "database": "feedlark",
        "collection": "feed",
        "query": {"url": url},
        "projection": {
            "_id": 1,
            "url": 1,
            "items": [{
                "link": 1,
                "pub_date": 1,
                "link": 1,
                "article_text": 1,
            }],
        },
    }))
    url_fields_gotten = gm_client.submit_job("db-get", to_get_urls_ids)
    bson_object = bson.BSON.decode(bson.BSON(url_fields_gotten.result))
    return bson_object["docs"]

# updates all of the item fields for all the unique feeds in the feeds db


def update_article_text(worker, job):
    log(0, "'update-all-article-text' initiated")
    try:
        bson_job_obj = bson.BSON.decode(bson.BSON(job.data))["url"]
        log(0, "Retrieving data from " + bson_job_obj + " item in db")
        feed_db_data = get_single_feed_db_data(bson_job_obj)[0]

    except Exception as e:
        log(2, e)
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))

    log(0, "db get complete")
    updated_item_list = []
    for db_item in feed_db_data['items']:
        if db_item['article_text'] != "":
            # If item in db already has article_text
            updated_item_list.append(db_item)
            continue
        else:
            # Runs if loop doesn't break, implying new item
            updated_item_list.append({
                'name': db_item['name'],
                'pub_date': db_item['pub_date'],
                'link': db_item['link'],
                'article_text': get_article_text(db_item['link'])
            })
    bson_data = None
    try:
        bson_data = bsonify_update_data(feed_db_data['_id'], feed_db_data[
                                        'url'], updated_item_list)
    except Exception as e:
        log(2, e)
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))
    log(0, "ready to db-update")
    update_response = None
    try:
        update_response = gm_client.submit_job(
            'db-update', str(bson_data), background=True)
    except Exception as e:
        log(2, e)
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))

    log(0, "update response: " + str(update_response))
    log(0, "'update-all-article-text' finished")
    return str(bson.BSON.encode({
        "status": "ok",
        "updated_feed": feed_db_data['_id'],
    }))

if __name__ == "__main__":
        # make the gearman worker to update feeds or add a new feed(adding not
        # done yet). Make the client to allow adder and getter job calls.
    log(0, "Initiating gearman worker")
    gm_worker = gearman.GearmanWorker(['localhost:4730'])
    log(0, "Initiating Client")
    gm_client = gearman.GearmanClient(["localhost:4730"])

    # register the tasks -> update all the article text for all feeds.
    log(0, "Registering task 'article-text-getter'")
    gm_worker.register_task('article-text-getter', update_article_text)
    gm_worker.work()
