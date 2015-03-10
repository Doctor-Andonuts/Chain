#!/usr/bin/python

#Imports
import json
from datetime import datetime
import sys

# TODO: Breaks if no dates
# Display some info from the JSON
def printChains():
	for chain in Chains:
		lastCompleted = datetime.strptime(chain['dates'][0], '%Y-%m-%d')
#		print "Chain Date: " + chain['dates'][0]
#		print "Chain Date: " + lastCompleted.strftime('%Y-%m-%d')
#		print "Today Date: " + datetime.now().strftime('%Y-%m-%d')

		daysSinceLastCompleted = (datetime.now() - lastCompleted).days

		if daysSinceLastCompleted > chain['maxDays']:
			message = "Do - Broken Chain"
		elif daysSinceLastCompleted == chain['maxDays']:
			message = "Do - Last Day"
		elif daysSinceLastCompleted >= chain['minDays']:
			message = "Should"
		elif daysSinceLastCompleted < chain['minDays']:
			message = "Wait"

		print '%s (%i-%i): %s' % (chain['name'],chain['minDays'],chain['maxDays'], message)

def deleteChain(filterId):
	for chain in Chains:
		if int(filterId) == int(chain['id']):
			Chains.remove(chain) 



#---------------------------



# Load json chain data from the datafile
with open('data.json') as JsonFile:
	Chains = json.load(JsonFile)

# Chains = list
# Chains[0] = dict
# Chains[0]['names'] = unicode
# Chains[0]['maxDays'] = unicode
# Chains[0]['minDays'] = unicode
# Chains[0]['dates'] = list



# Parse command line
if len(sys.argv) == 1:
	printChains()
else:
	if sys.argv[1] == 'add':
		print 'TODO: add'


		newDates = ['2015-03-09']
		newChain = {'name':'Test Name','minDays':5,'maxDays':6,'dates':newDates}
		Chains.append(newChain)



	elif sys.argv[2] == 'delete':
		deleteChain(sys.argv[1])
	elif sys.argv[2] == 'mod':
		print 'TODO: mod'
	elif sys.argv[2] == 'done':
		print 'TODO: done';
	else:
		print 'Syntax Error'






# Write my new JSON to file
with open('data.json', 'w') as outfile:
    json.dump(Chains, outfile)



