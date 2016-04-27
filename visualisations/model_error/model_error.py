import gearman
import bson
import sys
import pickle
import os
from random import shuffle
from sklearn import linear_model

# get kw_score module, so it doesn't need to do a gearman request for each call
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'aggregator'))
import kw_score

gearman_client = gearman.GearmanClient(['localhost:4730'])

def get_username_from_input(argv):
    '''
    A python script gives its input args as a list;
    Convert that list to a single string.
    '''
    return ' '.join(argv[1:])

def get_input_data(all_data):
    return [all_data[i][0] for i in xrange(len(all_data))]

def get_output_data(all_data):
    return [all_data[i][1] for i in xrange(len(all_data))]

def db_get(collection, query, projection):
    db_req = {
        'database': 'feedlark',
        'collection': collection,
        'query': query,
        'projection': projection
    }
    key = os.getenv('SECRETKEY')
    if key is not None:
        db_req['key'] = key
    str_bson_db_req = str(bson.BSON.encode(db_req))
    raw_db_result = gearman_client.submit_job('db-get', str_bson_db_req).result
    db_result = bson.BSON.decode(bson.BSON(raw_db_result))
    return db_result

def has_enough_classes(training):
    training_classes = set()
    for t in training:
        training_classes.add(t[1])
    return len(training_classes) >= 2

def get_model_score(training, validation):
    model = linear_model.SGDClassifier(loss='log', n_iter=5)
    model.fit(get_input_data(training), get_output_data(training))
    curr_score = model.score(get_input_data(validation), get_output_data(validation))
    return curr_score

def main():
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    if len(sys.argv) < 2:
        print('Please specify a user to get the error of. See README.md')
        return
    username = get_username_from_input(sys.argv)

    print 'Getting model error of {}'.format(username)
    print 'Loading user\'s votes from database'

    # get the user's votes on articles
    db_result = db_get('vote', {
        'username': username
    },{
        'article_url': 1,
        'feed_url': 1,
        'positive_opinion': 1,
        'vote_datetime': 1
    })
    if db_result['status'] != 'ok':
        print 'Error'
        print 'Could not get user data from vote collection'
        print db_result['description']
        return
    articles = db_result['docs']

    print len(articles), 'article opinions found in vote db for given user'

    # map each article url to 1 or -1, if the user liked or disliked it
    article_opinions = {}
    vote_datetimes = {}
    for article in articles:
        # make sure all the required fields are there
        req_fields = ['article_url', 'positive_opinion', 'vote_datetime']
        if not all([s in article for s in req_fields]):
            print 'Error'
            print 'Vote is missing some fields: {}'.format(article)
            continue
        url = article['article_url']
        # set the classes for the votes to 1 for positive and -1 for negative
        vote = 1 if article['positive_opinion'] else -1
        article_opinions[url] = vote
        vote_datetimes[url] = article['vote_datetime']

    # split the articles into the feeds they belong to, to minimise db lookups
    # the dict maps feed urls to a list of article urls fromt that feed
    feeds = {}
    for article in articles:
        if article['feed_url'] in feeds:
            feeds[article['feed_url']].append(article['article_url'])
        else:
            feeds[article['feed_url']] = [article['article_url']]

    # get a set of the unique article urls
    article_url_set = set(article_opinions.keys())
    print len(article_url_set), 'unique articles in set'

    if len(article_url_set) < 0:
        print 'Error'
        print 'Not enough articles in data set'
        return
    
    # get the words the user is interested in
    db_result = db_get('user', {
        'username': username
    }, {
        'words': 1
    })
    if db_result['status'] != 'ok':
        print 'Error'
        print 'Could not load data from user collection'
        print db_result['description']
        return
    if len(db_result['docs']) < 1:
        print 'Error'
        print 'No such user in user collection'
        return
    user_data = db_result['docs'][0]
    user_words = user_data['words']

    # it is required to have at least classes, so create two
    # inputs with extreme values to train the model 
    data_x = [[10.0, 1], [0.0, 10000000]]
    data_y = [1, -1]

    # get the data from the db for each feed a user voted on an article in
    for feed in feeds:
        db_result = db_get('feed', {
            'url': feed
        }, {
            'items': 1
        })
        if db_result['status'] != 'ok':
            print 'Error'
            print 'Could not get data from feed collection'
            print db_result['description']
            return
        if 'docs' not in db_result or len(db_result['docs']) < 1:
            print 'Error'
            print 'No feed returned for url', feed
            return

        items = db_result['docs'][0]['items']
        # check the items in that feed for one the user voted on
        for item in items:
            if item['link'] not in article_url_set:
                continue
            print 'adding', item['link']
            if 'topics' not in item:
                print 'Error'
                print 'No topics for given item, skipping'
                continue
            words = item['topics']
            topic_crossover = kw_score.score(words, user_words)
            if 'pub_date' not in item:
                print 'Error'
                print 'No pub_date for given item, skipping'
                continue
            time_diff = vote_datetimes[item['link']] - item['pub_date']
            x = [topic_crossover, time_diff.total_seconds()]
            y = article_opinions[item['link']]
            data_x.append(x)
            data_y.append(y)

        print 'Articles from feed', feed, 'added to data'
         

    print data_x
    print data_y
    
    if len(data_x) < 3:
        print 'Error'
        print 'Not enough data points'
        return
    
    data_points = [(data_x[i], data_y[i]) for i in xrange(len(data_x))]
    n = 0
    score = 0

    # start the 2-fold cross-validation, doing up to 10 folds of the data
    repetitions = min(len(data_points), 10)
    for k in xrange(repetitions):
        print 'Iteration {} out of {} ({}% finished)'.format(k, len(data_points), 100*(float(k)/repetitions))
        shuffle(data_points)
        training = data_points[:len(data_points)/2]
        validation = data_points[len(data_points)/2:]
        if has_enough_classes(training):
            curr_score = get_model_score(training, validation)
            print '- Score 1 this fold: {}'.format(curr_score)
            score += curr_score
            n += 1
        else:
            print '- Not enough training classes, skipping'
            continue 

        #swap the training and validation data
        training, validation = validation, training
        if has_enough_classes(training):
            curr_score = get_model_score(training, validation)
            print '- Score 2 this fold: {}'.format(curr_score)
            score += curr_score
            n += 1 
        else:
            print '- Not enough training classes, skipping'
            continue
    if n == 0:
        print 'Error'
        print 'Not enough valid data points'
        return
    print 'Score: {:.6f}, based on {} divisions of the data.'.format(float(score)/n, n)
    return

if __name__ == '__main__':
    main()
