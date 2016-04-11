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


def update_model(user_data, article_data, is_positive):
    """update the actual model in the user db with the new data"""
    model = None
    log(0, "Getting pickled model")
    if "model" not in user_data:
        log(1, "No model included in user data, creating new one.")
        model = linear_model.SGDClassifier(loss='log')
    else:
        try:
            pickled_model = user_data["model"]
            model = pickle.loads(pickled_model)
        except Exception as e:
            log(2, "Error depickling model: " + str(e))
            model = linear_model.SGDClassifier(loss='log')

    log(0, "Training model with new data")
    topic_crossover = 0 # a comparison of how close the articles are in terms of topic, taken from the worker in /aggregator
    log(0, str(user_data['words']))
    log(0, str(article_data['topics']))
    score_request = bson.BSON.encode({
        'key': key,
        'article_words': user_data['words'],
        'user_words': article_data['topics'],
        })
    score_response = gearman_client.submit_job('score', str(score_request))
    score_data = bson.BSON(score_response.result).decode()
    if score_data['status'] == 'ok':
        topic_crossover = score_data['score']
    else:
        log(2, "Error getting crossover score: " + str(score_data['description']))
    age = (datetime.now() - article_data['pub_date']).total_seconds()*1000 # get the number of millis in difference

    inputs = [topic_crossover, age]
    output = 0 if is_positive else 1
    log(0, str(inputs) + " " + str(output))
    try:
        model.partial_fit([inputs], [output], classes=[0, 1])
    except Exception as e:
        log(2, "Could not train model: " + str(e))

    log(0, "Repickling model")
    try:
        user_data['model'] = pickle.dumps(model)
    except Exception as e:
        log(2, "Error pickling model: " + str(e))
    return user_data


def add_update_to_db(data):
    """log the given user opinion to the vote db collection"""
    req_data = bson.BSON.encode({
        "key": key,
        "database": "feedlark",
        "collection": "vote",
        "data": data,
        })
    gearman_client.submit_job('db-add', str(req_data))


def update_user_data(username, updates):
    """update the db entry of the user with the given username, with the given dict of updates"""
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
    """Get the data of user from database"""
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


def update_user_model(worker, job):
    bson_input = bson.BSON(job.data)
    job_input = bson_input.decode()

    if key is not None:
        log(0, "Checking secret key")
        if 'key' not in job_input or job_input['key'] != key:
            log(2, "Secret key mismatch")
            response = bson.BSON.encode({
                'status': 'error',
                'description': 'Secret key mismatch',
                })
            return str(response)

    add_update_to_db(job_input)
    log(0, 'update-user-model called with data ' + str(job_input))
    if not ("username" in job_input and "feed_url" in job_input and "article_url" in job_input and "positive_opinion" in job_input):
        log(1, 'Missing field in input: ' + str(job_input))
        response = {"status":"error", "description":"Missing field in input."}
        bson_response = bson.BSON.encode(response)
        return str(bson_response)

    log(0, "Getting user data from db")
    user_data = get_user_data(job_input["username"])
    if user_data is None:
        response = {"status":"error", "description":"No user data received from db for user " + str(job_input["username"])}
        bson_response = bson.BSON.encode(response)
        return str(bson_response)
    
    log(0, "Getting feed data from db")
    feed_data = get_feed_data(job_input["feed_url"])
    if feed_data is None:
        response = {"status":"error", "description":"No feed data receieved from db for feed " + str(job_input["feed_url"])}
        bson_response = bson.BSON.encode(response)
        return str(bson_response)

    log(0, "Updating topic weights")
    user_words = user_data['words']
    for item in feed_data['items']:
        if item['link'] == job_input['article_url']:
            if not 'topics' in item:
                log(1, "No topics associated with given article.")
                break
            topics = item['topics']
            user_words = update_topic_counts(user_words, topics, job_input['positive_opinion'])
            user_data = update_model(user_data, item, job_input["positive_opinion"]) # update the pickled user model
            break
    
    log(0, "Updating user db with new topic weights")
    user_data['words'] = user_words
    update_user_data(job_input['username'], user_data)
    log(0, "Worker finished.")
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
    gearman_worker.set_client_id('update-user-model')
    gearman_worker.register_task('update-user-model', update_user_model)
    gearman_worker.work()
