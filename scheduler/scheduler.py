import gearman
import bson
import datetime
import time
import os
import urllib2


def log(level, message):
    """Log information as specified in feedlark specs"""
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    curr_time = str(datetime.datetime.now()).replace('-', '/')[:-7]
    print curr_time, levels[level], message

delay = 300
gm_client = gearman.GearmanClient(['localhost:4730'])

key = os.getenv('SECRETKEY')
if key is not None:
    request = bson.BSON.encode({
        'key': key,
        })
else:
    request = bson.BSON.encode({})

while True:
    log(0, "Updating all feeds...")
    gm_client.submit_job('update-all-feeds',str(request))

    #Once scraper is done aggregate
    log(0, "Aggregating...")
    gm_client.submit_job('aggregate',str(request))

    #Now send out summary emails
    log(0, "Sending summary emails")
    urllib2.urlopen("http://localhost:3000/user/summaries/" + key).close()

    log(0, "Sleeping for {} seconds".format(delay))
    time.sleep(delay)
