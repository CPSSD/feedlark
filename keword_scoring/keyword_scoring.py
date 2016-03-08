import gearman
import BSON

def log(message, level=0):
    levels = ['INFO:','WARNING:','ERROR:']
    time = str(datetime.now()).replace('-','/')[:-7]
    print time,levels[level],message

def score_keywords(worker, job):
    pass


log("Initiating gearman client")
gm_client = gearman.GearmanClient(['localhost:4730'])
log("Initiating gearman worker")
gm_worker = gearman.GearmanWorker(['localhost:4730'])

log("Registering task 'score-keywords'")
gm_worker.register_task('score-keywords', score_keywords)
gm_worker.work()
