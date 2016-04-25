import gearman
import bson
import pickle
from datetime import datetime
from os import getenv

from sklearn import linear_model

gearman_client = None
key = getenv('SECRETKEY')


def log(level, message):
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    time = datetime.now().strftime('%H:%M %d/%m/%Y')
    print(str(time) + " " + levels[level] + " " + str(message))


def update_topic_counts(old_topics, changes, is_positive):
    """modify the user topic weights to reflect the new data"""
    diff = 1 if is_positive else -1
    for change in changes:
        if change in old_topics:
            old_topics[change] += diff
        else:
            old_topics[change] = diff
    return old_topics


def add_update_to_db(data):
    """
    log the given user opinion to the vote db collection
    """
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "vote",
        "data": data,
        })
    gearman_client.submit_job('db-add', str(req_data))


def update_user_data(username, updates):
    """
    Update the data for the given user in the database,
    with the given dict of updates
    """
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "user",
        "data": {
            "selector": {
                "username": username,
                },
            "updates": updates,
            },
        })
    update_rsp = gearman_client.submit_job('db-update', str(req_data))
    result = bson.BSON(update_rsp.result).decode()
    if result[u"status"] != u"ok":
        log(2, "Error updating user data: " + str(result))


def get_user_data(username):
    """
    Get the data of user from database
    """
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "user",
        "query": {
            "username": username,
            },
        "projection": {},
        })
    query_rsp = gearman_client.submit_job('db-get', str(req_data))
    result = bson.BSON(query_rsp.result).decode()
    if result[u"status"] != u"ok":
        log(2, "Error getting database entry for user " + str(username))
        return None
    if "docs" not in result:
        log(1, "No 'docs' field in results for user " + str(username))
        return None
    if len(result["docs"]) == 0:
        log(1, "No docs returned for user " + str(username))
        return None
    return result["docs"][0]


def get_feed_data(feed_url):
    """Get the data of a given feed"""
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "feed",
        "query": {
            "url": feed_url,
            },
        "projection": {},
        })
    get_response = gearman_client.submit_job('db-get', str(req_data))
    result = bson.BSON(get_response.result).decode()
    if result[u"status"] != u"ok":
        log(2, "Error getting database entry for feed " + str(feed_url))
        return None
    if "docs" not in result or len(result["docs"]) == 0:
        log(1, "No docs returned for feed " + str(feed_url))
        return None
    return result["docs"][0]

def vote_already_exists(username, article_url):
    '''
    Check if the user with the given username
    has already voted on the specified article.
    Returns True or False
    '''
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "vote",
        "query": {
            "$and": [{
                    "article_url": article_url,
                    },{
                    "username": username
                    }
                ]
            },
        "projection": {}
        })
    get_response = gearman_client.submit_job('db-get', str(req_data))
    result = bson.BSON(get_response.result).decode()
    if result['status'] != 'ok':
        log(2, 'Error getting votes for user {} for article {}'.format(username, article_url))
        return False
    return 'docs' in result and len(result['docs']) > 0


def register_vote(worker, job):
    """
    Gearman entry point
    """
    bson_input = bson.BSON(job.data)
    job_input = bson_input.decode()


    # auth check
    if key is not None:
        if 'key' not in job_input or job_input['key'] != key:
            log(2, "Secret key mismatch")
            response = bson.BSON.encode({
                'status': 'error',
                'description': 'Secret key mismatch',
                })
            return str(response)

    if vote_already_exists(job_input['username'], job_input['article_url']):
        log(1, 'User already voted on this article')
        response = bson.BSON.encode({
            'status': 'error',
            'description': 'User already voted on this article'
            })
        return str(response)
    # log the vote
    job_input['vote_datetime'] = datetime.now()
    add_update_to_db(job_input)

    required_fields = ['username', 'feed_url', 'article_url', 'positive_opinion']
    if not (all([x in job_input for x in required_fields])):
        log(1, 'Missing field in input: ' + str(job_input))
        response = {
            "status":"error",
            "description":"Missing field in input."
        }
        bson_response = bson.BSON.encode(response)
        return str(bson_response)

    log(0, "'register-vote' called for user '{}' for article {}".format(job_input['username'], job_input['article_url']))

    # fetch that user's info from the database
    user_data = get_user_data(job_input["username"])
    if user_data is None:
        log(1, "No user data received from db for user " + str(job_input['username']))
        response = {
            "status":"error",
            "description":"No user data received from db for user " + str(job_input["username"])
        }
        bson_response = bson.BSON.encode(response)
        return str(bson_response)

    # fetch that feed's info from the database
    feed_data = get_feed_data(job_input["feed_url"])
    if feed_data is None:
        log(1, "No feed data received from db for feed " + str(job_input['feed_url']))
        response = {
            "status":"error",
            "description":"No feed data receieved from db for feed " + str(job_input["feed_url"])
        }
        bson_response = bson.BSON.encode(response)
        return str(bson_response)

    # get the user's interest words
    user_words = None
    if "words" in user_data:
        user_words = user_data['words']
    else:
        user_data['words'] = {}
        user_words = {}

    for item in feed_data['items']:

        if item['link'] == job_input['article_url']:
            log(0, "found feed")
            if not 'topics' in item:
                log(1, "No topics associated with given article.")
                break
            topics = item['topics']
            user_words = update_topic_counts(user_words, topics, job_input['positive_opinion'])
            break

    # put the user's new interest words back into their dict
    user_data['words'] = user_words
    
    # put it all back in the database
    update_user_data(job_input['username'], user_data)
    response = {"status":"ok"}
    bson_response = bson.BSON.encode(response)
    return str(bson_response)


def init_gearman_client():
    global gearman_client
    log(0, "Creating gearman client.")
    gearman_client = gearman.GearmanClient(['localhost:4730'])

if __name__ == '__main__':
    init_gearman_client()
    log(0, "Creating gearman worker 'update-user-model'")
    gearman_worker = gearman.GearmanWorker(['localhost:4730'])
    gearman_worker.set_client_id('register-vote')
    gearman_worker.register_task('register-vote', register_vote)
    gearman_worker.work()
