import gearman
from bson import BSON

def log(message, level=0):
    levels = ['INFO:','WARNING:','ERROR:']
    time = str(datetime.now()).replace('-','/')[:-7]
    print time,levels[level],message

def get_feed_db_data(url):
    # format the request
    data_request = str(BSON.encode({
        "database":"feedlark",
        "collection":"feed",
        "query": {'url':url},
        "projection":{
            "_id":1,
            "url":1,
            "items":1,
            },
        }))
    response = gm_client.submit_job("db-get", data_request)
    db_data = BSON.decode(BSON(response.result))

    return db_data["docs"]

def get_user_db_data(username):
    # format the request
    data_request = str(BSON.encode({
        "database":"feedlark",
        "collection":"user",
        "query": {'username':username},
        "projection":{
            "_id":1,
            "username":1,
            "words":1,
            },
        }))
    response = gm_client.submit_job("db-get", data_request)
    db_data = BSON.decode(BSON(response.result))

    return db_data["docs"]

def score_keywords(worker, job):
    log("'score-keywords' initiated")
    try:
        feed_url = BSON.decode(BSON(job.data))['url']
        username = BSON.decode(BSON(job.data))['username']
    except:
        log("Error when reading job data: "+job.data,2)
        error = {
            'status':'error',
            'data':'Invalid parameters',
            }
        return str(BSON.encode(error))

    try:
        log("Getting feed from feed db")
        feed_data = get_feed_db_data(feed_url)[0]
        log("Getting user from user db")
        user_data = get_user_db_data(username)[0]
    except:
        log("Error when getting db data",2)
        error = {
            'status':'error',
            'data':'Error getting DB data',
            }
        return str(BSON.encode(error))

    

    
    

log("Initiating gearman client")
gm_client = gearman.GearmanClient(['localhost:4730'])
log("Initiating gearman worker")
gm_worker = gearman.GearmanWorker(['localhost:4730'])

log("Registering task 'score-keywords'")
gm_worker.register_task('score-keywords', score_keywords)
gm_worker.work()
