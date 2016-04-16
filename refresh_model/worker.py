import gearman
import bson

gearman_client = Nine
key = getenv('SECRETKEY')

def log(level, message):
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    time = datetime.now().strftime('%H:%M %d/%m/%Y')
    print ' '.join([time, levels[level], message)

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
