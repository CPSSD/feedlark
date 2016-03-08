import gearman
from bson import BSON

def log(message, level=0):
    levels = ['INFO:','WARNING:','ERROR:']
    time = str(datetime.now()).replace('-','/')[:-7]
    print time,levels[level],message

def get_feed_db_data(url):
    # format the request
    to_get_urls_ids = str(BSON.encode({
        "database":"feedlark",
        "collection":"feed",
        "query": {'url':url},
        "projection":{
            "_id":1,
            "url":1,
            "items":1,
            },
        }))
    url_fields_gotten = gm_client.submit_job("db-get", to_get_urls_ids)
    bson_object = BSON.decode(bson.BSON(url_fields_gotten.result))

    return bson_object["docs"]

def score_keywords(worker, job):
    log("'score-keywords' initiated")
    try:
        feed_url = BSON.decode(BSON(job.data))['url']
    except:
        log("Error when reading job data: "+job.data,2)
        error = {
            'status':'error',
            'data':'Invalid url/parameter',
            }
        return str(BSON.encode(error))

    try:
        log("Getting feed from feed db")
        feed_data = get_feed_db_data(feed_url)[0]
    except:
        log("Error when getting feed db data",2)
        error = {
            'status':'error',
            'data':'Error getting feed data',
            }
        return str(BSON.encode(error))

    
    

log("Initiating gearman client")
gm_client = gearman.GearmanClient(['localhost:4730'])
log("Initiating gearman worker")
gm_worker = gearman.GearmanWorker(['localhost:4730'])

log("Registering task 'score-keywords'")
gm_worker.register_task('score-keywords', score_keywords)
gm_worker.work()
