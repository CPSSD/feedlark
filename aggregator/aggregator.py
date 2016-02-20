import gearman,sys
import bson

class Aggregator:

    def __init__(self, gm_client):
        self.gm_client = gm_client

    
    def get_feed_items(self, feed_url):
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
                '_id':0,
                },
            })

        #submit_job as below is blocking
        gm_job = self.gm_client.submit_job('db-get',str(request))
        return bson.BSON(gm_job.result).decode()['docs'][0]['items']


    def get_users(self):
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
        gm_job = self.gm_client.submit_job('db-get',str(request))
        return bson.BSON(gm_job.result).decode()['docs']


    def put_g2g(self, username, data):
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

        gm_job = self.gm_client.submit_job('db-upsert',str(request))
        if bson.BSON(gm_job.result).decode()['status'] != 'ok':
            print "Adding to g2g failed"
            print "Status: " + bson.BSON(gm_job.result).decode()['status']

        return


    def aggregate(self, gearman_worker, gearman_job):
        print "Job recieved"
        print "Loading users from 'user' database"
        user_data = self.get_users()

        for user in user_data:
            print "\nLoading feeds for:", user['username']
            user_g2g = {'username':user['username'],'feeds':[]}

            for feed_url in user['subscribed_feeds']:
                print "--> ", feed_url
                for item in self.get_feed_items(feed_url):
                    user_g2g['feeds'].append(
                        {
                            'feed':feed_url,
                            'name':item['name'],
                            'link':item['link'],
                            'pub_date':item['pub_date'],
                        })
                    
            print "Sorting items"
            user_g2g['feeds'] = sorted(user_g2g['feeds'],key=lambda x:x['pub_date'],reverse=True)
            print "Putting items in 'g2g' database"
            self.put_g2g(user['username'], user_g2g)
            print "Completed"

        return "SUCCESS"

if __name__ == '__main__':
    agg = Aggregator(gearman.GearmanClient(['localhost:4730']))

    gm_worker = gearman.GearmanWorker(['localhost:4730'])
    gm_worker.set_client_id('aggregator')
    gm_worker.register_task('aggregate', agg.aggregate)
    print "Reistered 'aggregate' task"

    gm_worker.work()
