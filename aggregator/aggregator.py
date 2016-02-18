import gearman
import bson

def get_feed_items(gm_client, feed_url):
    '''
    This takes a url and returns the matching document in the feeds database.
    '''
    request = bson.BSON.encode({
        'database':'feedlark',
        'collection':'feeds',
        'query':{
            'url':feed_url,
            },
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',request)
    return bson.BSON.decode(gm_job.result)['docs']['items']

def get_users(gm_client):
    '''
    Returns a list of all the user documents in the user database.
    The documents returned contain only the username and subscribed_feeds.
    '''
    request = bson.BSON.encode({
        'database':'feedlark',
        'collection':'users',
        'query':'',
        'projection':{
            'username':1,
            'subscribed_feeds':1,
            },
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',request)
    return bson.BSON.decode(gm_job.result)['docs']

def get_g2g_id(gm_client, username):
    request = bson.BSON.encode({
        'database':'feedlark',
        'collection':'g2g',
        'query':{
            'username':username,
            },
        'projection':{
            '_id':1,
            },
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',request)

    #Pull out the first result's _id
    return_doc = bson.BSON.decode(gm_job.result)['docs']
    if return_doc == []:
        return -1
    else:
        return return_doc[0]['_id']

def put_g2g(gm_client, object_id, data):
    if object_id == -1:
        request = bson.BSON.encode({
            'database':'feedlark',
            'collection':'g2g',
            'data':data,
            })

        gm_job = gm_client.submit_job('db-add',request)        

    else:
        request = bson.BSON.encode({
            'database':'feedlark',
            'collection':'g2g',
            'data':{
                'updates':data,
                'id':object_id,
                },
            })

        gm_job = gm_client.submit_job('db-add',request)


def aggregate(gearman_worker, gearman_job):
    gm_client = gearman.GearmanClient(['localhost:4730'])
    user_data = get_users(gm_client)

    for user in user_data:
        user_g2g = {'username':user['username'],'feeds':[]}

        for feed_url in user['subscribed_feeds']:
            user_g2g['feeds'].extend([
                {
                    'feed':feed['url'],
                    'name':item['name'],
                    'link':item['link'],
                    'pub_date':item['pub_date'],
                } for item in get_feed_items(gm_client, feed_url)]
                                     )
        user_g2g['feeds'] = sorted(user_g2g['feeds'],key=lambda x:x['pub_date'])

        user_obj_id = get_g2g_id(gm_client, user['username'])
        put_g2g(gm_client, user_obj_id, user_g2g)

    return "SUCCESS"


gm_worker = gearman.GearmanWorker(['localhost:4730'])
gm_worker.set_client_id('aggregator')
gm_worker.register_task('aggregate', aggregate)

gm_worker.work()
