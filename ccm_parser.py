import csv
import json


assignment_list = {'Countries':[], 'AMAZON':[],'DEGAULLE':[],'CAP':[],'FIFA':[],'RFE':[],'AD HOC':[],'IRAN':[],'IRAQ':[],'1984':[],'BNW':[],'Orange 1':[],'Orange 2':[],'Mughal':[],'UNSC':[]}
ionic_list = []
num_assignments = 0
total_num_delegates = 0
committees_ionic = {}

def create_assignment(committee_name, assignment):
	#print "Creating assignment for %s, %s, %s" % (school_name, committee_name, assignment)
	global num_assignments, assignment_list, total_num_delegates
	num_assignments += 1

	# Only SOCHUM and WHS are double-delegate committees
	# add the specific side to the assignment
	assignment_list[committee_name].append(assignment)


# Write out the assignments to some file
def printassignment(assignment_list):
	for key in assignment_list:
		assignment_list[key].sort()
		print '("' + key + '", ('
		for item in assignment_list[key]:
			print '		("' + item + '", u"' + item + '"), '
		print "		)"
		print "),"



reader = csv.reader(open('tmp/ccm/UpdatedCCM.csv', 'rU'))


for i, row in enumerate(reader):
	# read header row and get all committees
	country = row[0]
	print country
	if country != "":
		create_assignment('Countries', country)


reader = csv.reader(open('tmp/ccm/UpdatedCCM_Characters.csv', 'rU'))

for i, row in enumerate(reader):
	# read header row and get all committees
	if i == 0:
		committee_header = row
		print committee_header
	else:
		for j in range(0, len(row)):
			if row[j]:
				print row[j]
				create_assignment(committee_header[j], row[j].strip('"').strip())

printassignment(assignment_list)
