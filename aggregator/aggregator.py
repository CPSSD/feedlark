from datetime import datetime
import gearman
import bson


def log(*message, **kwargs):
    '''
    Logs to stdout

    Pass in parameters as you would the python3 print function.
    Includes the optional 'level' keyword argument, defaults to 0.
    '''
    level = kwargs['level'] if 'level' in kwargs else 0
    levels = ['INFO:', 'WARNING:', 'ERROR:']

    message_str = ''.join(map(str, message))
    time = str(datetime.now()).replace('-', '/')[:-7]

    print time, levels[level], message_str


class Aggregator:

    def __init__(self, gm_client):
        self.gm_client = gm_client

    def get_feed_items(self, feed_url):
        '''
        This takes a url and returns the matching document in the feeds
        database.
        '''
        request = bson.BSON.encode({
            'database': 'feedlark',
            'collection': 'feed',
            'query': {
                'url': feed_url,
                },
            'projection': {
                '_id': 0,
                },
            })

        # submit_job as below is blocking
        gm_job = self.gm_client.submit_job('db-get', str(request))
        return bson.BSON(gm_job.result).decode()['docs'][0]['items']

    def get_users(self):
        '''
        Returns a list of all the user documents in the user database.
        The documents returned contain only the username and subscribed_feeds.
        '''
        request = bson.BSON.encode({
            'database': 'feedlark',
            'collection': 'user',
            'query': {},
            'projection': {
                'username': 1,
                'subscribed_feeds': 1,
                'words': 1,
                },
            })

        # submit_job as below is blocking
        gm_job = self.gm_client.submit_job('db-get', str(request))
        return bson.BSON(gm_job.result).decode()['docs']

    def put_g2g(self, username, data):
        '''
        Adds sorted items to g2g database for a given user.
        '''
        request = bson.BSON.encode({
            'database': 'feedlark',
            'collection': 'g2g',
            'data': {
                'updates': data,
                'selector': {
                    'username': username,
                    },
                },
            })

        gm_job = self.gm_client.submit_job('db-upsert', str(request))
        if bson.BSON(gm_job.result).decode()['status'] != 'ok':
            log("Adding to g2g failed", level=2)
            log("Status: ", bson.BSON(gm_job.result).decode()['status'])

        return

    def aggregate(self, gearman_worker, gearman_job):
        log("Job recieved")
        log("Loading users from 'user' database")
        user_data = self.get_users()

        for user in user_data:
            log("Loading feeds for: ", user['username'])
            user_g2g = {'username': user['username'], 'feeds': []}

            for feed_url in user['subscribed_feeds']:
                log("--> ", feed_url)
                for item in self.get_feed_items(feed_url):
                    user_g2g['feeds'].append(
                        {
                            'feed': feed_url,
                            'name': item['name'],
                            'link': item['link'],
                            'word_crossover':
                                score(item['topics'], user['words']),
                            'pub_date': item['pub_date'],
                        })

            log("Normalising dates")
            oldest = min(user_g2g['feeds'], key=lambda x: x['pub_date'])
            newest = max(user_g2g['feeds'], key=lambda x: x['pub_date'])
            normalised_items = []
            for item in user_g2g['feeds']:
                item['norm_date'] = (item['pub_date']-oldest)/float(newest-oldest)
                normalised_items.append(item)
            user_g2g['feeds'] = normalised_items

            log("Sorting items")
            user_g2g['feeds'] = sorted(
                user_g2g['feeds'],
                key=lambda x: x['pub_date']+x['word_crossover'],
                reverse=True)
            log("Putting items in 'g2g' database")
            self.put_g2g(user['username'], user_g2g)
            log("Completed")

        return str(bson.BSON.encode({'status': 'ok'}))

if __name__ == '__main__':
    agg = Aggregator(gearman.GearmanClient(['localhost:4730']))

    gm_worker = gearman.GearmanWorker(['localhost:4730'])
    gm_worker.set_client_id('aggregator')
    gm_worker.register_task('aggregate', agg.aggregate)
    log("Reistered 'aggregate' task")

    gm_worker.work()
