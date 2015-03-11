#!/usr/bin/python

#Imports 
import os
import json
from datetime import datetime
from datetime import timedelta
import sys

class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

# Display some info from the JSON
def printChains():
	screenRows, screenColumns = os.popen('stty size', 'r').read().split()


# Determine rows and columns of screen
# Determine how long the longest chain name is
# Figure out how many days I can fit with the rest of the screen
	
	longestNameLength = 4;
	longestMinLength = 1;
	longestMaxLength = 1;
	for chain in Chains:
		if len(chain['name']) > longestNameLength:
			longestNameLength = len(chain['name'])
		if len(str(chain['minDays'])) > longestMinLength:
			longestMinLength = len(str(chain['minDays']))
		if len(str(chain['maxDays'])) > longestMaxLength:
			longestMaxLength = len(str(chain['maxDays']))

	daysLength = longestMinLength + longestMaxLength + 3
	
	header =  color.UNDERLINE + "Name".ljust(longestNameLength) + color.END + " "
	header += color.UNDERLINE + "Days".ljust(daysLength) + color.END + " "
	
	today = datetime.now()
	dateHeader = ""
	for i in range(0,14):
		dateDiff = timedelta(days=i)
		dateHeader += color.UNDERLINE + (today - dateDiff).strftime('%d') + color.END + " "
	print header + dateHeader

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

		chainName =  chain['name'].ljust(longestNameLength)
		chainDays = "(" + str(chain['minDays']) + "-" + str(chain['maxDays']) + ")"


		print chainName + " " + chainDays.center(daysLength)



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
with open('data.json', 'a+') as JsonFile: # This creates a new file if one did not exist
	try:
		Chains = json.load(JsonFile)
	except ValueError, e:
		Chains = []


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



