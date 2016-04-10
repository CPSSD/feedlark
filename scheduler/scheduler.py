import gearman
import bson
import time
import os

gm_client = gearman.GearmanClient(['localhost:4730'])

key = os.getenv('SECRETKEY')
if key is not None:
    request = bson.BSON.encode({
        'key': key,
        })
else:
    request = bson.BSON.encode({})

while True:
    gm_client.submit_job('update-all-feeds', str(request))

    # Once scraper is done aggregate
    gm_client.submit_job('aggregate', str(request))
    time.sleep(30)
