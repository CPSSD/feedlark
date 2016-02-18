import gearman
import pymongo
import bson # the pymongo bson lib

print "Starting python worker 'db-get'"
print "Initiating gearman worker"
gearman_worker = gearman.GearmanWorker(["localhost:4731"])
print "Initiating mongo client"
mongo_client = pymongo.MongoClient('localhost', 27017)

def task_listener_db_getter(worker, job):
    print "Worker initiated: "
    if not bson.is_valid(job.data):
        print "Error: invalid bson"
        return bson.BSON.encode({"status":"error", "error":"invalid bson"})
    bsonObj = bson.BSON(job.data)
    #data = bson.BSON.decode(bsonObj)
    data = bsonObj.decode()
    db = data["database"]
    coll = data["collection"]
    query = data["query"]
    projection = {}
    if "projection" in data:
        projection = data["projection"]
    print "getting db"
    docs = mongo_client[db][coll].find(query, projection)
    resultDocs = []
    index = 0
    for doc in docs:
        resultDocs.append(doc)
    results = {"docs":resultDocs}
    print "results"
    print results
    resultBson = bson.BSON.encode(results)
    print str(resultBson)
    print bson.BSON.decode(resultBson)
    return str(resultBson)

class test_object:
    def __init__(self):
        self.data = bson.BSON.encode({"database":"feedlark", "collection":"feeds", "query":{}, "projection":{"_id":1, "url": 1}})
#        self.data = '{"database":"feedlark"}'

test_job = test_object()
print test_job.data
print task_listener_db_getter(None, test_job)

print "Registering worker"
gearman_worker.set_client_id("python-db-getter")
print "Registering task 'db-get'"
gearman_worker.register_task("db-get", task_listener_db_getter)

gearman_worker.work()
