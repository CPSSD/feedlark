import gearman
import bson

def get_feed_items(gm_client, feed_url):
    '''
    This takes a url and returns the matching document in the feeds database.
    '''
    request = bson.BSON.encode({
        'database':'feedlark',
        'collection':'feed',
        'query':{
            'url':feed_url,
            },
        'projection':{
            '_id':1,
            },
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',str(request))
    return bson.BSON(gm_job.result).decode()['docs']['items']


def get_users(gm_client):
    '''
    Returns a list of all the user documents in the user database.
    The documents returned contain only the username and subscribed_feeds.
    '''
    request = bson.BSON.encode({
        'database':'feedlark',
        'collection':'user',
        'query':{},
        'projection':{
            'username':1,
            'subscribed_feeds':1,
            },
        })

    #submit_job as below is blocking
    gm_job = gm_client.submit_job('db-get',str(request))
    return bson.BSON(gm_job.result).decode()['docs']


def put_g2g(gm_client, username, data):
    '''
    Adds sorted items to g2g database for a given user.
    '''
    request = bson.BSON.encode({
        'database':'feedlark',
        'collection':'g2g',
        'data':{
            'updates':data,
            'selector':{
                'username':username,
                },
            },
        })

    gm_job = gm_client.submit_job('db-update',str(request))
    if bson.BSON(gm_job.result).decode()['status'] != 'ok':
        print "Adding to g2g failed"
        print "Status: " + bson.BSON(gm_job.result).decode()['status']

    return


def aggregate(gearman_worker, gearman_job):
    print "Job recieved"
    gm_client = gearman.GearmanClient(['localhost:4730'])
    print "Loading users from 'user' database"
    user_data = get_users(gm_client)

    for user in user_data:
        print "\nLoading feeds for: ", user['username']
        user_g2g = {'username':user['username'],'feeds':[]}

        for feed_url in user['subscribed_feeds']:
            print "--> ", feed_url
            for item in get_feed_items(gm_client, feed_url):
                user_g2g['feeds'].append(
                    {
                        'feed':feed_url,
                        'name':item['name'],
                        'link':item['link'],
                        'pub_date':item['pub_date'],
                    })
                
        print "Sorting items"
        user_g2g['feeds'] = sorted(user_g2g['feeds'],key=lambda x:x['pub_date'])
        print "Putting items in 'g2g' database"
        put_g2g(gm_client, user['username'], user_g2g)
        print "Completed"

    return "SUCCESS"


gm_worker = gearman.GearmanWorker(['localhost:4730'])
gm_worker.set_client_id('aggregator')
gm_worker.register_task('aggregate', aggregate)
print "Reistered 'aggregate' task"

gm_worker.work()
