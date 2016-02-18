import gearman
import pymongo
import json

print "Starting python worker 'db-get'"
print "Initiating gearman worker"
gearman_worker = gearman.GearmanWorker(["localhost:4730"])
print "Initiating mongo client"
mongo_client = pymongo.MongoClient('localhost', 27017)

def task_listener_db_getter(worker, job):
    print "Worker initiated"
    print "Worker initiated: "
    data = json.loads(job.data)
    print data
    db = data["database"]
    coll = data["collection"]
    query = data["query"]
    projection = {}
    if "projection" in data:
        projection = data["projection"]
    print "getting db"
    docs = mongo_client[db][coll].find(query, projection)
    print str(docs)
    results = "{\"docs\"=["
    index = 0
    for doc in docs:
        print doc
        if index > 0:
            results += ","
        results += str(doc)
        index += 1
    results += "]}"
    print "results:"
    print results
    return results

print "Registering worker"
gearman_worker.set_client_id("python-db-getter")
print "Registering task 'db-get'"
gearman_worker.register_task("db-get", task_listener_db_getter)

gearman_worker.work()
