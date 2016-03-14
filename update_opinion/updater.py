import gearman
import bson
from datetime import datetime

gearman_client = None

def log(level, message):
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    time = datetime.now().strftime('%H:%M %d/%m/%Y')
    print(str(time) + " " + levels[level] + " " + str(message))

def update_topic_counts(old_topics, changes, is_positive):
    diff = 1 if is_positive else -1
    for change in changes:
        if change in old_topics:
            old_topics[change] += diff
        else:
            old_topics[change] = diff
    return old_topics

def add_update_to_db(data):
    req_data = {"database":"feedlark", "collection":"votes", "data":data}
    bson_req = bson.BSON.encode(req_data)
    gearman_client.submit_job('db-add', str(bson_req))

def update_user_model(worker, job):
    bson_input = bson.BSON(job.data)
    input = bson_input.decode()
    add_update_to_db(input)
    log(0, 'update-user-model called with data ' + str(input))
    if not ("username" in input and "feed_url" in input and "article_url" in input):
        log(1, 'Missing field in input: ' + str(input))
        response = {"status":"error", "description":"Missing field in input."}
        bson_response = bson.BSON.encode(response)
        return str(bson_response)
    response = {"status":"ok"}
    bson_response = bson.BSON.encode(response)
    return str(bson_response)

if __name__ == '__main__':
    log(0, "Creating gearman client.")
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    log(0, "Creating gearman worker 'update-user-model'")
    gearman_worker = gearman.GearmanWorker(['localhost:4730'])
    gearman_worker.set_client_id('update-user-model')
    gearman_worker.register_task('update-user-model', update_user_model)
    gearman_worker.work()
