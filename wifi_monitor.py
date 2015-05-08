import requests
import json
import os
import pymongo

if 'MONGO_URI' in os.environ:
	db = pymongo.MongoClient(os.environ['MONGO_URI']).brown
else:
    print "The database URI's environment variable was not found."

locations = {'andrews', 'littlejo', 'ratty', 'vdubs', 'blueroom'}

def get_recent_measurements(location):
	return json.loads(requests.get("https://i2s.brown.edu/wap/apis/localities/" + location + "/devices?history=true").content)

def put_measurement_into_db(measurement):
	measurement['timestamp'] = float(measurement['timestamp'])	# convert timestamp to float
	measurement_query = {'locality': measurement['locality'],
						 'timestamp': measurement['timestamp']}
	db.wifi.update(measurement_query, measurement, upsert=True)

for location in locations:
	print "Gathering WiFi measurements for location:", location
	for measurement in get_recent_measurements(location):
		put_measurement_into_db(measurement)
		print "Added measurement:", str(measurement)

print "Finished gathering WiFi measurements."