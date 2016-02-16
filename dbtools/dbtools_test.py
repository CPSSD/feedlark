import gearman

client = gearman.GearmanClient(['localhost:4730'])
req = client.submit_job('db-get', '{"database":"feedlark", "collection":"feeds", "query":{}}')
print req.result
