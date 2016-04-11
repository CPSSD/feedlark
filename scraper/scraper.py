import sys
import requests
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime
from os import getenv
import bson
import gearman

assert (2, 5) <= sys.version_info <= (3, 0)


def get_feed_data(rss_url):
    '''
    Returns a list of dictionaries.
    Each dictionary corresponds to a item in the feed.

    Each item contains a name, link, and date published.
    '''
    if type(rss_url) != str and type(rss_url) != unicode:
        raise TypeError('URL must be a string')

    feed = feedparser.parse(rss_url)
    items_list = []
    for item in feed['entries']:
        date = item['published_parsed'] if 'published_parsed' in item else item[
            'updated_parsed']
        items_list.append({
            'name': item['title'],
            'link': item['link'],
            'pub_date': datetime(*date[:6]),
        })
    return items_list


def log(level, message):
    """Log information as specified in feedlark specs"""
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    time = str(datetime.now()).replace('-', '/')[:-7]
    print time, levels[level], message


def bsonify_update_data(item_id, url, all_data):
    """Convert given data to bson in valid format for db-update"""
    items_list = {
        "key": key,
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


def get_all_feed_docs():
    """Submits a job to 'db-get' to get all ids and urls of the feeds"""
    # format the request
    to_get_urls_ids = str(bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "feed",
        "query": {},
        "projection": {
            "_id": 1,
            "url": 1,
            "items": 1,
        },
    }))
    url_fields_gotten = gm_client.submit_job("db-get", to_get_urls_ids)
    bson_object = bson.BSON.decode(bson.BSON(url_fields_gotten.result))

    return bson_object["docs"]


def get_single_feed_doc(url):
    """Submits a job to 'db-get' to a specific feed"""
    to_get_urls_ids = str(bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "feed",
        "query": {
            "url": url
        },
        "projection": {
            "_id": 1,
            "url": 1,
            "items": 1,
        },
    }))
    url_fields_gotten = gm_client.submit_job("db-get", to_get_urls_ids)
    bson_object = bson.BSON.decode(bson.BSON(url_fields_gotten.result))

    return bson_object["docs"]


def gather_updates(doc):
    """Expects a doc as returned by get_feed"""
    log(0, "Loading items in feed: " + doc['url'])
    updated_item_list = []
    result = get_feed_data(doc['url'])  # list of item dicts
    log(0, "Parsed feed " + doc['url'])
    for item in result:
        for db_item in doc['items']:
            if item['link'] == db_item['link']:
                # If item already in db
                updated_item_list.append(db_item)
                break
        else:
            # Runs if loop doesn't break, implying new item
            updated_item_list.append({
                'name': item['name'],
                'pub_date': item['pub_date'],
                'link': item['link'],
                'article_text': '',
            })
    log(0, "Gathered list of items to update for: " + doc['url'])
    return updated_item_list


def update_database(doc, updated_item_list):
    """Updates the database, given a doc and updated_item_list"""
    bson_data = None
    try:
        bson_data = bsonify_update_data(doc['_id'], doc['url'], updated_item_list)
    except Exception as e:
        log(2, str(e))
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))

    log(0, "ready to db-update")
    update_response = None
    try:
        update_response = gm_client.submit_job('db-update', str(bson_data), background=True)
    except Exception as e:
        log(2, str(e))
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))
    log(0, "update response: " + str(update_response))

    log(0, "Submitting items for scraping")
    # Submit items for scraping
    text_getter_data = str(bson.BSON.encode({
        "key": key,
        "url": doc['url'],
        }))
    try:
        update_response = gm_client.submit_job(
            'article-text-getter', text_getter_data, background=True)
    except Exception as e:
        log(2, str(e))
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))
    log(0, "article-text-getter update response: " + str(update_response))


def update_single_feed(worker, job):
    log(0, "'update-single-feed' initiated")

    try:
        request = bson.BSON(job.data).decode()
        url = request['url']
    except:
        log(2, "Invalid parameters provided")
        return str(bson.BSON.encode({
            'status': 'error',
            'error-description': 'Invalid parameters',
            }))

    if key is not None:
        log(0, "Checking secret key")
        if 'key' not in request or request['key'] != key:
            log(2, "Secret key mismatch")
            response = bson.BSON.encode({
                'status': 'error',
                'description': 'Secret key mismatch',
                })
            return str(response)

    try:
        feed = get_single_feed_doc(url)
        updated_feeds = gather_updates(feed[0])
        log(0, "'update-single-feed' finished gathering updates, applying")
        update_database(feed[0], updated_feeds)
    except Exception as e:
        log(2, "'update-single-feed' failed")
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))

    log(0, "'update-single-feed' finished")
    return str(bson.BSON.encode({
        "status": "ok",
        "updated_feeds": [x['_id'] for x in feed],
    }))


# updates all of the item fields for all the unique feeds in the feeds db
def update_all_feeds(worker, job):
    log(0, "'update-all-feeds' initiated")

    if key is not None:
        log(0, "Checking secret key")
        request = bson.BSON(job.data).decode()
        if 'key' not in request or request['key'] != key:
            log(2, "Secret key mismatch")
            response = bson.BSON.encode({
                'status': 'error',
                'description': 'Secret key mismatch',
                })
            return str(response)

    log(0, "Retrieving data from feed db")
    feed_db_data = get_all_feed_docs()

    try:
        for doc in feed_db_data:
            updated_feeds = gather_updates(doc)
            update_database(doc, updated_feeds)
    except Exception as e:
        log(2, "'update-all-feeds' failed")
        return str(bson.BSON.encode({
            "status": "error",
            "error-description": str(e)
        }))

    log(0, "'update-all-feeds' finished")
    return str(bson.BSON.encode({
        "status": "ok",
        "updated_feeds": [x['_id'] for x in feed_db_data],
    }))
    return str(bson.BSON.encode({"status": "ok"}))

# Get secret key, must be global.
key = getenv('SECRETKEY')

if __name__ == "__main__":
    log(0, "Initiating gearman worker")
    gm_worker = gearman.GearmanWorker(['localhost:4730'])

    log(0, "Initiating gearman client")
    # This is global and required by get_all_feed_docs
    gm_client = gearman.GearmanClient(["localhost:4730"])

    log(0, "Registering task 'update-all-feeds'")
    gm_worker.register_task('update-all-feeds', update_all_feeds)
    log(0, "Registering task 'update-singlefeed'")
    gm_worker.register_task('update-single-feed', update_single_feed)

    gm_worker.work()
