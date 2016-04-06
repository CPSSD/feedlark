import gearman
import bson
import sys
import pickle
import os
from sklearn import linear_model

# import ../../aggregator/kw_score.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'aggregator'))
import kw_score

gearman_client = gearman.GearmanClient(['localhost:4730'])

def get_username_from_input(argv):
    return ' '.join(argv[1:])

def db_get(collection, query, projection):
    db_req = {
        'database': 'feedlark',
        'collection': collection,
        'query': query,
        'projection': projection
    }
    str_bson_db_req = str(bson.BSON.encode(db_req))
    raw_db_result = gearman_client.submit_job('db-get', str_bson_db_req).result
    db_result = bson.BSON.decode(bson.BSON(raw_db_result))
    return db_result

def main():
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    if len(sys.argv) < 2:
        print('Please specify a user to get the error of. See README.md')
        return
    username = get_username_from_input(sys.argv)

    # get the user's votes on articles
    db_result = db_get('vote', {
        'username': username
    },{
        'article_url': 1,
        'feed_url': 1,
        'positive_opinion': 1
    })
    if db_result['status'] != 'ok':
        print 'Error'
        print 'Could not get user data from vote collection'
        print db_result['description']
        return
    articles = db_result['docs']

    print len(articles), 'article opinions found in vote db for given user'

    # map each article url to 1 or 0, if the user liked or disliked it
    article_opinions = {}
    for article in articles:
        if not ('article_url' in article and 'positive_opinion' in article):
            continue
        url = article['article_url']
        vote = 1 if article['positive_opinion'] else 0
        article_opinions[url] = vote

    # split the articles into the feeds they belong to, to minimise db lookups
    feeds = {}
    for article in articles:
        if article['feed_url'] in feeds:
            feeds[article['feed_url']].append(article['article_url'])
        else:
            feeds[article['feed_url']] = [article['article_url']]

    # get a set of the unique article urls
    #article_url_set = set([a['article_url'] for a in articles])
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

    # the inputs and outputs we have for the prediction
    data_x = [[10.0], [0.0]]
    data_y = [1, 0]

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
        for item in items:
            if item['link'] not in article_url_set:
                continue
            words = item['topics']
            topic_crossover = kw_score.fast_score(words, user_words)
            x = [topic_crossover]
            y = article_opinions[item['link']]
            data_x.append(x)
            data_y.append(y)
            print item['link'], 'added'

        print 'Articles from feed', feed, 'added to data'
         

    print data_x
    print data_y

    print 'Training model with 90% of data, testing with 10%'
    num_train = len(data_x)*9/10
    print num_train, 'data points in training set'
    train_x = data_x[:num_train]
    train_y = data_y[:num_train]
    print train_x
    print train_y
    test_x = data_x[num_train:]
    test_y = data_y[num_train:]

    model = linear_model.SGDClassifier(loss='log')
    model.fit(train_x, train_y)
    score = model.score(test_x, test_y)
    print 'Score =', score
            

if __name__ == '__main__':
    main()
