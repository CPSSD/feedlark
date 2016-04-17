import gearman
import bson
from os import getenv
from datetime import datetime

gearman_client = None
key = getenv('SECRETKEY')

def log(level, message):
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    time = datetime.now().strftime('%H:%M %d/%m/%Y')
    print ' '.join([time, levels[level], message])

def get_user_data(username):
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "user",
        "query": {
            "username": username
        },
        "projection": {}
    })
    get_response = gearman_client.submit_job('db-get', str(req_data))
    result = bson.BSON(get_response.result).decode()
    if result['status'] != 'ok':
        log(2, "Error getting db entry for user {}".format(username))
        return None
    if "docs" not in result or len(result['docs']) == 0:
        log(1, "No docs returned for user {}".format(username))
        return None
    return result['docs'][0]

def update_user_data(username, data):
    '''
    Update the document for the given user,
    With the dict of updates provided in `data`
    '''
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "user",
        "data":{
            "updates": data,
            "selector":{
                "username": username
            }
        }
    }
    update_response = gearman_client.submit_job('db-update', str(req_data))
    result = bson.BSON(update_response.result).decode()
    if result['status'] != 'ok':
        log(2, 'Error updating db entry for user {}'.format(username))
        return

def get_votes_for_user(username):
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "vote",
        "query": {
            "username": username
        },
        "projection": {}
    })
    get_response = gearman_client.submit_job('db-get', str(req_data))
    result = bson.BSON(get_response).decode()
    if result['status'] != 'ok':
        log(2, "Error getting votes for user {}".format(username))
        return
    if 'docs' not in result:
        log(1, "No docs returned for user {}".format(username))
        return None
    return result['docs']

def get_feed_items(feed_url, item_urls):
    '''
    Fetches the data for each article with its url in item_urls,
    From the feed with the url feed_url
    '''
    return []

def build_model(user_data, votes):
    '''
    Build a model for the user with the given data,
    Using the information in the `votes` list
    '''
    # create a dict of lsts, mapping each feed to the items to be
    # taken from that feed to create the votes
    feed_items = {}
    item_opinion = {}
    for vote in votes:
        feed_url = vote['feed_url']
        article_url = vote['article_url']
        if vote['feed_url'] in feed_items:
            feed_items[feed_url].append(article_url)
        else:
            feed_items[feed_url] = [article_url]
        item_opinion[article_url] = 1 if vote['positive_opinion'] else -1

    x = []
    y = []

    for feed in feed_items:
        for item in get_feed_items(feed, feed_items[feed]):
            inputs = []
            # inputs[0] should be the topic crossover
            # inputs[1] should be the datetime diff
            x.append(inputs)
            y.append(item_opinion[item])

def refresh_model(worker, job):
    """
    Gearman entry point
    """
    bson_input = bson.BSON(job.data)
    job_input = bson_input.decode()

def init_gearman_client():
    global gearman_client
    log(0, 'Creating gearman client')
    gearman_client = gearman.GearmanClient(['localhost:4730'])

if __name__ == '__main__':
    init_gearman_client()
    log(0, "Creating gearman worker 'refresh-model'")
    gearman_worker = gearman.GearmanWorker(['localhost:4730'])
    gearman_worker.set_client_id('refresh-model')
    gearman_worker.register_task('refresh-model', refresh_model)
    gearman_worker.work()
