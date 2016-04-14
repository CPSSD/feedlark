import gearman
import datetime
import time


def log(level, message):
    """Log information as specified in feedlark specs"""
    levels = ['INFO:', 'WARNING:', 'ERROR:']
    curr_time = str(datetime.datetime.now()).replace('-', '/')[:-7]
    print curr_time, levels[level], message

delay = 300
gm_client = gearman.GearmanClient(['localhost:4730'])
while True:
    log(0, "Updating all feeds...")
    gm_client.submit_job('update-all-feeds','')

    #Once scraper is done aggregate
    log(0, "Aggregating...")
    gm_client.submit_job('aggregate','')

    log(0, "Sleeping for {} seconds".format(delay))
    time.sleep(delay)
