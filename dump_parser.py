import csv
import json


data = []
avoid_list = ["contenttypes.contenttype", "sessions.session", "djcelery.taskmeta", "transport.message", "transport.queue", "admin.logentry"]

reader = json.load(open('backup.json'))


for row in reader:
	# read header row and get all committees
	if row["model"] not in avoid_list:
		data.append(row)

# Write out the assignments to some file
json.dump(data, open('backup_fixed.json', 'w'),
    indent=4)
