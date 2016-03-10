import gearman
import bson

# Example of how to update all-feeds
gm_client = gearman.GearmanClient(["localhost:4730"])
go_ahead = "{}"
update = gm_client.submit_job("update-all-feeds", go_ahead)
print bson.BSON.decode(bson.BSON(update.result))
