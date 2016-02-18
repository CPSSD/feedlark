import gearman
import time

gm_client = gearman.GearmanClient(['localhost:4730'])
while True:
    gm_client.submit_job('update-all-feeds','')

    #Once scraper is done aggregate
    gm_client.submit_job('aggregate','')
    time.sleep(30)
