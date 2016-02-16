import gearman
import json

def get_feed_items(gm_client, feed_url):
    '''
    This takes a url and returns the matching document in the feeds database.
    '''
    request = json.dumps({
        'database':'feedlark',
        'collection':'feeds',
        'query':{
            'url':feed_url,
            },
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',request)
    return json.loads(gm_job.result)['docs']['items']

def get_users(gm_client):
    '''
    Returns a list of all the user documents in the user database.
    The documents returned contain only the username and subscribed_feeds.
    '''
    request = json.dumps({
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
    return json.loads(gm_job.result)['docs']

def put_g2g(data):
    pass

def aggregate(gearman_worker, gearman_job):
    gm_client = gearman.GearmanClient(['localhost:4730'])
    user_data = get_users(gm_client)

    g2g_data = []
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
        g2g_data.append(user_g2g)

    put_g2g(g2g_data)
    return "SUCCESS"


gm_worker = gearman.GearmanWorker(['localhost:4730'])
gm_worker.set_client_id('aggregator')
gm_worker.register_task('aggregate', aggregate)

gm_worker.work()
    
