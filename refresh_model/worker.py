import gearman
import bson
from os import getenv
from datetime import datetime
from sklearn import linear_model
import pickle

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
        log(2, result['description'])
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
    })
    update_response = gearman_client.submit_job('db-update', str(req_data))
    result = bson.BSON(update_response.result).decode()
    if result['status'] != 'ok':
        log(2, 'Error updating db entry for user {}'.format(username))
        log(2, result['description'])
        return

def get_votes_for_user(username):
    '''
    Get all the votes that this user has cast on articles
    '''
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
    result = bson.BSON(get_response.result).decode()
    if result['status'] != 'ok':
        log(2, "Error getting votes for user {}".format(username))
        log(2, result['description'])
        return None
    if 'docs' not in result or len(result['docs']) == 0:
        log(1, "No docs returned for user {}".format(username))
        return None
    return result['docs']

def get_feed_items(feed_url, item_urls):
    '''
    Fetches the data for each article with its url in item_urls,
    From the feed with the url feed_url
    '''
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "feed",
        "query":{
            "url": feed_url
        },
        "projection": {
            "items": 1
        }
    })
    get_response = gearman_client.submit_job('db-get', str(req_data))
    result = bson.BSON(get_response.result).decode()
    if result['status'] != 'ok':
        log(2, 'Error getting feed {}'.format(feed_url))
        log(2, result['description'])
        return None
    if 'docs' not in result or len(result['docs']) == 0:
        log(1, 'No docs returned for feed {}'.format(feed_url))
        return None
    item_url_set = set(item_urls)
    response = [d for d in result['docs'][0]['items'] if ('link' in d and d['link'] in item_url_set)]
    return response

def get_topic_crossover(user_data, article_data):
    '''
    Given the user data and article data,
    returns the crossover according to the 'score' gearman worker
    '''
    req_data = bson.BSON.encode({
        "key": key,
        "article_words": article_data['topics'],
        "user_words": user_data['words']
    })
    gearman_response = gearman_client.submit_job('score', str(req_data))
    result = bson.BSON(gearman_response).decode()
    if result['status'] != 'ok':
        log(2, 'Error getting topic crossover score')
        log(2, result['description'])
        return None
    ans = result['score']
    return ans

def build_model(user_data, votes):
    '''
    Build a model for the user with the given data,
    Using the information in the `votes` list
    '''
    # create a dict of lsts, mapping each feed to the items to be
    # taken from that feed to create the votes
    feed_items = {}
    item_opinion = {}
    item_vote_datetime = {}
    if len(votes) == 0:
        return None
    log(0, 'Building model for user {} with {} votes'.format(user_data['username'], len(votes)))
    log(0, str(votes))
    for vote in votes:
        feed_url = vote['feed_url']
        article_url = vote['article_url']
        item_vote_datetime[article_url] = vote['vote_datetime']

        if vote['feed_url'] in feed_items:
            feed_items[feed_url].append(article_url)
        else:
            feed_items[feed_url] = [article_url]

        item_opinion[article_url] = 1 if vote['positive_opinion'] else -1

    log(0, '{}\n{}\n{}'.format(feed_items, item_opinion, item_vote_datetime))
    x = []
    y = []

    model = linear_model.SGDClassifier(loss="log", n_iter=5)

    for feed in feed_items:
        for item in get_feed_items(feed, feed_items[feed]):
            inputs = []
            # inputs[0] should be the topic crossover
            inputs.append(get_topic_crossover(user_data, item))
            # inputs[1] should be the diff between
            # the vote datetime and the article datetime
            inputs.append(item_vote_datetime[item['link']] - item['pub_date'])
            x.append(inputs)
            y.append(item_opinion[item])

    if len(x) != len(y):
        log(2, 'Mismatch in input and output length:')
        log(2, str(x))
        log(2, str(y))
        return None

    model.fit(x, y)
    pickled_model = pickle.dumps(model)
    return pickled_model

def refresh_model(worker, job):
    """
    Gearman entry point
    """
    bson_input = bson.BSON(job.data)
    job_input = bson_input.decode()

    if key is not None:
        if 'key' not in job_input or job_input['key'] != key:
            log(2, 'Secret key mismatch')
            return str(bson.BSON.encode({
                'status': 'error',
                'description': 'Secret key mismatch'
                }))

    if 'username' not in job_input:
        log(2, 'No username supplied')
        return str(bson.BSON.encode({
            'status': 'error',
            'description': 'No username supplied'
            }))

    username = job_input['username']
    log(0, 'Refreshing model for user {}'.format(username))

    user_data = get_user_data(username)
    if user_data is None:
        log(2, 'No data recieved from db for given username')
        return str(bson.BSON.encode({
            'status': 'error',
            'description': 'No data recieved from db for given username'
            }))

    votes = get_votes_for_user(username)
    if votes is None or len(votes) == 0:
        log(1, 'No vote data found for given username')
        return str(bson.BSON.encode({
            'status': 'error',
            'description': 'No vote data found for given username'
            }))

    new_model = build_model(user_data, votes)
    user_data['model'] = new_model
    update_user_data(username, user_data)

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
