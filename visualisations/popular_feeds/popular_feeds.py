import sys
import gearman
import bson
import os

def make_list_feeds(users):
    feed_count = {}
    for user in users:
        for feed in user["subscribed_feeds"]:
            if feed in feed_count:
                feed_count[feed] += 1
            else:
                feed_count[feed] = 1
    return feed_count

def main():
    if len(sys.argv) != 2:
        print 'This tool takes 1 command line argument; the number of topics to output data on. See README.md'
        return
    num_requested_feeds = int(sys.argv[1])
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    result = bson.BSON.decode(bson.BSON(gearman_client.submit_job('db-get', str(bson.BSON.encode({
        'key': os.getenv('SECRETKEY'),
        'database':'feedlark',
        'collection':'user',
        'query':{},
        'projection':{
            'subscribed_feeds':1
        }
    }))).result))

    if result[u'status'] == u'ok':
        # add the feeds to a dictionary as keys with count as variables
        feed_counts = make_list_feeds(result["docs"])
        sorted_feed = sorted(feed_counts,reverse=True)

        #get ouput ready
        output = []
        output.append(str(len(feed_counts)))

        if num_requested_feeds > len(sorted_feed):
            num_requested_feeds = len(sorted_feed)

        for i in xrange(num_requested_feeds):
            output.append(sorted_feed[i] + " " + str(feed_counts[sorted_feed[i]]))
        output = "\n".join(output)
        # output to file
        f = open("most_popular_feeds.txt", "w")
        f.write(output)
        f.close()

    else:
        print 'Error getting user data from database'
        print result['description']
        return

if __name__ == "__main__":
    main()
