import csv
import json


assignment_list = []
ionic_list = []
num_assignments = 0
total_num_delegates = 0
committees = json.load(open('committees/committees.json'))
committees_ionic = {}

for key in committees:
	committees_ionic[key] = { "positions": [], "messages": [] }


def create_assignment(committee_name, assignment):
	#print "Creating assignment for %s, %s, %s" % (school_name, committee_name, assignment)
	global num_assignments, assignment_list, total_num_delegates
	num_assignments += 1

	# Only SOCHUM and WHS are double-delegate committees
	# add the specific side to the assignment
	committee_id = committees[committee_name]
	print committee_name + " - " + assignment
	assignment_list.append({
		"pk": num_assignments,
		"model": "committees.countrycharactermatrix", 
		"fields": {
			"position": assignment, 
			"committee": committee_id,
		}
	})
	committees_ionic[committee_name]["positions"].append(assignment)


reader = csv.reader(open('tmp/ccm/ccm-country.csv', 'rU'))


for i, row in enumerate(reader):
	# read header row and get all committees
	if i == 0:
		committee_header = row[1:]
		print committee_header
	else:
		country = row[0]
		flag = row[1:]
		for j in range(0, len(flag)):
			if flag[j] == '1':
				create_assignment(committee_header[j], country)


reader = csv.reader(open('tmp/ccm/ccm-character.csv', 'rU'))

for i, row in enumerate(reader):
	# read header row and get all committees
	if i == 0:
		committee_header = row
		print committee_header
	else:
		for j in range(0, len(row)):
			if row[j]:
				create_assignment(committee_header[j], row[j].strip('"').strip())


# Write out the assignments to some file
json.dump(assignment_list, open('tmp/ccm/matrix.json', 'w'),
    indent=4)
json.dump(committees_ionic, open('tmp/ccm/matrix_ionic.json', 'w'),
	indent=4)
