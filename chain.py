#!/usr/bin/python
# coding: utf-8

#Imports 
import os
import json
from datetime import datetime
from datetime import timedelta
import sys

# Configuration
CompletedCharacter = "X"
SpacingCharacter = u"ˑ"  # Triangle
NotRequiredCharacter = "*"
NeedToDoCharacter = "O"
daysToShow = 10


class color:
	UNDERLINE = '\033[4m'
	END = '\033[0m'
today = datetime.now()


def printLine(lineData, lengths, isHeader=0):
	if isHeader:
		formatStart = color.UNDERLINE
		formatEnd = color.END
	else:
		formatStart = ""
		formatEnd = ""

	line = formatStart + lineData['id'].rjust(lengths['id']) + formatEnd + " "
	line += formatStart + lineData['name'].ljust(lengths['name']) + formatEnd + " "
	line += formatStart + lineData['days'].ljust(lengths['days']) + formatEnd + " "
	for key in lineData['data']:
		line += formatStart + lineData['data'][key].rjust(2) + formatEnd + " "
	
	print line

	

# Display some info from the JSON
def printChains():
	
	# Get longest length of names, minDays, and maxDays
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

	# Save them for passing into print functions
	lengths = {}
	lengths['id'] = 2
	lengths['name'] = longestNameLength
	lengths['days'] = longestMinLength + longestMaxLength + 3 # For (-)

	# Save header data to print
	headerLine = {}
	headerLine['id'] = 'Id'
	headerLine['name'] = 'Name'
	headerLine['days'] = 'Days'
	headerLine['data'] = {}

	# Grab the date info for the header as well 
	today = datetime.now()
	for i in xrange(daysToShow):
		dateDiff = timedelta(days=i)
		headerLine['data'][i] = (today - dateDiff).strftime('%d')

	# Print Header
	printLine(headerLine, lengths, 1) 

	# Get Chain info
	for chain in Chains:
		chainData = {}
		chainData['id'] = str(chain['id'])
		chainData['name'] = chain['name']
		chainData['days'] = "(" + str(chain['minDays']) + "-" + str(chain['maxDays']) + ")"
		chainData['data'] = {}

		for i in xrange(daysToShow):
			dateDiff = timedelta(days=i)
			dateTest = (today - dateDiff).strftime('%Y-%m-%d')
			if dateTest in chain['dates']:
				chainData['data'][i] = CompletedCharacter
			else:
				chainData['data'][i] = SpacingCharacter

		# Print Chain info
		printLine(chainData, lengths)	


def deleteChain(filterId):
	for chain in Chains:
		if int(filterId) == int(chain['id']):
			Chains.remove(chain) 


def addChain(newChainName, newChainMinDays, newChainMaxDays):
	newDates = []
	newChainId = 0
	for chain in Chains:
		if chain['id'] > newChainId:
			newChainId = int(chain['id'])
		newChainId += 1
	newChain = {'id':newChainId,'name':newChainName,'minDays':int(newChainMinDays),'maxDays':int(newChainMaxDays),'dates':newDates}
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


homedir = os.path.expanduser('~')
# Load json chain data from the datafile
with open(homedir + '/.chain.json', 'a+') as JsonFile: # This creates a new file if one did not exist
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
			doneDate = today.strftime("%Y-%m-%d")
		else:
			doneDate = sys.argv[3]
		markChainDone(sys.argv[1], doneDate)
	else:
		print 'Syntax Error'


# Write my new JSON to file
with open(homedir + '/.chain.json', 'w') as outfile:
	json.dump(Chains, outfile)



