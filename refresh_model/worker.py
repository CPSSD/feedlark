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
