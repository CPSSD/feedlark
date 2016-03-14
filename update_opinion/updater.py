import gearman
import bson
from datetime import datetime

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

gearman_client = None

def update_user_model(worker, job):
    bson_input = bson.BSON(job.data)
    input = bson_input.decode()

if __name__ == '__main__':
    log(0, "Creating gearman client.")
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    log(0, "Creating gearman worker 'update-user-model'")
    gearman_worker = gearman.GearmanWorker(['localhost:4730'])
    gearman_worker.set_client_id('update-user-model')
    gearman_worker.register_task('update-user-model', update_user_model)
    gearman_worker.work()
