import gearman
import bson
import unittest
from subprocess import call
from time import time

class TestDbTools(unittest.TestCase):
    def setUp(self):
        self.client = gearman.GearmanClient(['localhost:4730'])

    def test_adder(self):
        req = {"database":"testing", "collection":"unit_tests", "data":{"inserttime":time(), "test":"adder"}}
        bsonReq = bson.BSON.encode(req)
        raw_response = self.client.submit_job('db-add', str(bsonReq))
        resp = bson.BSON.decode(bson.BSON(raw_response.result))
        self.assertTrue("status" in resp)
        self.assertEquals(resp["status"], "ok")

    def test_updater(self):
        req = {"database":"testing", "collection":"unit_tests", "data":{"inserttime":time(), "has_been_updated":False, "test":"updater"}}
        bsonReq = bson.BSON.encode(req)
        raw_response = self.client.submit_job('db-add', str(bsonReq))
        resp = bson.BSON.decode(bson.BSON(raw_response.result))
        ident = resp["_id"]
        req = {"database":"testing", "collection":"unit_tests", "data":{"selector":{"_id":ident}, "updates":{"has_been_updated":True}}}
        bsonReq = bson.BSON.encode(req)
        raw_response = self.client.submit_job('db-update', str(bsonReq))
        resp = bson.BSON.decode(bson.BSON(raw_response.result))
        self.assertTrue("status" in resp)
        self.assertEquals(resp["status"], "ok")

    def test_getter(self):
        ident = bson.objectid.ObjectId() 
        req = {"database":"testing", "collection":"unit_tests", "data":{u"_id":ident, u"inserttime":time(), u"test": u"getter"}}
        bsonReq = bson.BSON.encode(req)
        raw_response = self.client.submit_job('db-add', str(bsonReq))

        get_req = {"database":"testing", "collection":"unit_tests", "query": { "_id":ident}, "projection":{"inserttime":1}}
        bsonReq = bson.BSON.encode(get_req)
        raw_response = self.client.submit_job('db-get', str(bsonReq))
        resp = bson.BSON.decode(bson.BSON(raw_response.result))
        self.assertTrue("status" in resp)
        self.assertEquals(resp["status"], "ok")
        self.assertEquals(len(resp["docs"]),  1)
        self.assertEquals(resp["docs"][0]["inserttime"], req["data"]["inserttime"])
        


if __name__ == '__main__':
    #set the gearman workers running
    #call("pwd")
    #call("python getter/getter.py &")
    #call("go run start_workers.go &")

    unittest.main()
