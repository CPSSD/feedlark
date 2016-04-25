from datetime import datetime
import gearman
import bson
from os import getenv
from predict import Classification


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

    def __init__(self, gm_client, key):
        self.gm_client = gm_client
        self.key = key

    def get_feed_items(self, feed_url):
        '''
        This takes a url and returns the matching document in the feeds
        database.
        '''
        request = bson.BSON.encode({
            'key': self.key,
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
            'key': self.key,
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
            'key': self.key,
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

    def get_score(self, topic, words):
        request = bson.BSON.encode({
            'key': self.key,
            'user_words': words,
            'article_words': topic,
            })

        gm_job = self.gm_client.submit_job('score', str(request))
        result = bson.BSON(gm_job.result).decode()
        if result['status'] != 'ok':
            log("Scoring article failed", level=1)
            log('Description: ' + result['description'], level=1)
            return 0

        return result['score']

    def aggregate(self, gearman_worker, gearman_job):
        log("Job recieved")
        if self.key is not None:
            request = bson.BSON(gearman_job.data).decode()
            if 'key' not in request or self.key != request['key']:
                log('Secret key mismatch', 2)
                response = bson.BSON.encode({
                    'status': 'error',
                    'description': 'Secret key mismatch',
                    })
                return str(response)

        log("Loading users from 'user' database")
        user_data = self.get_users()

        for user in user_data:
            log('=====================================')
            log("Loading feeds for: ", user['username'])
            user_g2g = {'username': user['username'], 'feeds': []}

            for feed_url in user['subscribed_feeds']:
                log("--> ", feed_url)
                for item in self.get_feed_items(feed_url):
                    word_crossover = 0
                    if 'topics' in item and 'words' in user:
                        word_crossover = self.get_score(
                            item['topics'],
                            user['words'],
                            )

                    user_g2g['feeds'].append(
                        {
                            'feed': feed_url,
                            'name': item['name'],
                            'link': item['link'],
                            'word_crossover': word_crossover,
                            'pub_date': item['pub_date'],
                        })

            if 'feeds' not in user_g2g or user_g2g['feeds'] == []:
                log('No feed items for user', level=1)
                log('Completed')
                continue

            try:
                log("Calculating dates")
                oldest = min(user_g2g['feeds'], key=lambda x: x['pub_date'])
                oldest = float(oldest['pub_date'].strftime('%s'))
                newest = max(user_g2g['feeds'], key=lambda x: x['pub_date'])
                newest = float(newest['pub_date'].strftime('%s'))

                normalised_items = []
                for item in user_g2g['feeds']:
                    item_seconds = float(item['pub_date'].strftime('%s'))
                    item['norm_date'] = (item_seconds-oldest)/(newest-oldest)
                    item['datetime_diff'] = (datetime.now() - item['pub_date']).total_seconds()
                    normalised_items.append(item)
                user_g2g['feeds'] = normalised_items
            except:
                log('Error processing dates (bad date formats?)', level=1)
                continue

            if 'model' in user_data:
                # sort the user's feed based on their ML model
                classifier = Classifier()
                classifier.load_model(user_data['model'])
                log("Model loaded, sorting items")
                # give the inputs [crossover, date diff] to the classifier
                sorter = lambda x: classifier.predict([
                    x['word_crossover'],
                    x['datetime_diff']])
                user_g2g['feeds'] = sorted(
                    user_g2g['feeds'],
                    key = sorter,
                    reverse=True)
            else:
                # there has to be a method to sort their items if they have no ML model
                # as the machine learning is being done in batches, and the user should
                # not have to wait a long time before their feed is visible
                log("No model for user: " + str(user['username']) + \
                    ", sorting items using non-ML method", level=1)
                user_g2g['feeds'] = sorted(
                    user_g2g['feeds'],
                    key=lambda x: x['norm_date']+x['word_crossover'],
                    reverse=True)
            log("Putting items in 'g2g' database")
            self.put_g2g(user['username'], user_g2g)
            log("Completed")

        return str(bson.BSON.encode({'status': 'ok'}))

if __name__ == '__main__':
    key = getenv('SECRETKEY')
    agg = Aggregator(gearman.GearmanClient(['localhost:4730']), key)

    gm_worker = gearman.GearmanWorker(['localhost:4730'])
    gm_worker.set_client_id('aggregator')
    gm_worker.register_task('aggregate', agg.aggregate)
    log("Registered 'aggregate' task")

    gm_worker.work()
