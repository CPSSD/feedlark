import gearman
import json

def get_rss(gm_client):
    request = json.dumps({
        'database':'feedlark',
        'collection':'feeds',
        'query':'',
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',request)
    return json.loads(gm_job.result)

def get_user(gm_client):
    request = json.dumps({
        'database':'feedlark',
        'collection':'users',
        'query':''
        'projection':{
            'username':1,
            'email':1,
            'subscribed_feeds':1,
            }
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',request)
    return json.loads(gm_job.result)

def put_g2g(data):
    pass

def aggregate():
    gm_client = gearman.GearmanClient(['localhost:4730'])
    
