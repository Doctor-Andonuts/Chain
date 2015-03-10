#!/usr/bin/python

#Imports
import json
from datetime import datetime
import sys

# Display some info from the JSON
def printChains():
	for chain in Chains:
		if len(chain['dates']) > 0:
			lastCompleted = datetime.strptime(chain['dates'][0], '%Y-%m-%d')

			daysSinceLastCompleted = (datetime.now() - lastCompleted).days
	
			if daysSinceLastCompleted > chain['maxDays']:
				message = "Do - Broken Chain"
			elif daysSinceLastCompleted == chain['maxDays']:
				message = "Do - Last Day"
			elif daysSinceLastCompleted >= chain['minDays']:
				message = "Should"
			elif daysSinceLastCompleted < chain['minDays']:
				message = "Wait"
		else:
			message = "Do - First Complete not done"

		print '%s (%i-%i): %s' % (chain['name'],chain['minDays'],chain['maxDays'], message)

def deleteChain(filterId):
	for chain in Chains:
		if int(filterId) == int(chain['id']):
			Chains.remove(chain) 


def addChain(newChainName, newChainMinDays, newChainMaxDays):
	newDates = []
	newChain = {'name':newChainName,'minDays':int(newChainMinDays),'maxDays':int(newChainMaxDays),'dates':newDates}
	Chains.append(newChain)

def modChain(chainId, chainName, chainMinDays, chainMaxDays):
        for chain in Chains:
                if int(chainId) == int(chain['id']):
			chain['name'] = chainName
			chain['minDays'] = int(chainMinDays)
			chain['maxDays'] = int(chainMaxDays)
			

def markChainDone(filterId, doneDate):
	 for chain in Chains:
                if int(filterId) == int(chain['id']):
			chain['dates'].append(doneDate)
			chain['dates'].sort(reverse=True)
			

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
		addChain(sys.argv[2], sys.argv[3], sys.argv[4])
	elif sys.argv[2] == 'delete':
		deleteChain(sys.argv[1])
	elif sys.argv[2] == 'mod':
		modChain(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])
	elif sys.argv[2] == 'done':
		if len(sys.argv) <= 3:
			today = datetime.now()
			doneDate = today.strftime("%Y-%m-%d")
		else:
			doneDate = sys.argv[3]
		markChainDone(sys.argv[1], doneDate)
	else:
		print 'Syntax Error'


# Write my new JSON to file
with open('data.json', 'w') as outfile:
    json.dump(Chains, outfile)



