#!/usr/bin/python
# coding: utf-8

#Imports 
import os
import json
from datetime import datetime
from datetime import timedelta
import sys


class color:
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	DARK_GREEN = '\033[48;5;22m'
	LIGHT_GREEN = '\033[48;5;2m'
	RED = '\033[48;5;88m'
	YELLOW = '\033[48;5;226m'

today = datetime.now()


# Configuration
CompletedCharacter = color.LIGHT_GREEN + "  " + color.END
NotRequiredCharacter = color.DARK_GREEN + "  " + color.END
ShouldDoCharacter = color.YELLOW + "  " + color.END
NeedToDoCharacter = color.RED + "  " + color.END
SpacingCharacter = " "
daysToShow = 7


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
	line += formatStart + lineData['length'].rjust(3) + formatEnd + " "
	for key in lineData['data']:
		line += formatStart + lineData['data'][key].rjust(2) + formatEnd + " "
	
	print line


def testChainLength(checkDate, chain, chainComboStart):
	for i in xrange(1, chain['maxDays']+1):
		testDate = checkDate - timedelta(days = i)
		if testDate.strftime('%Y-%m-%d') in chain['dates']:
			chainComboStart = testChainLength(testDate, chain, testDate)
			break
	return chainComboStart


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
	headerLine['length'] = 'Len'
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
		chainDisplay = {}
		chainDisplay['id'] = str(chain['id'])
		chainDisplay['name'] = chain['name']
		chainDisplay['days'] = "(" + str(chain['minDays']) + "-" + str(chain['maxDays']) + ")"
		chainDisplay['data'] = {}

		chainComboAdd = 0
		for i in xrange(daysToShow):
			dateDiffDelta = timedelta(days=i)
			dateTest = (today - dateDiffDelta).strftime('%Y-%m-%d')
			if dateTest in chain['dates']:
				chainDisplay['data'][i] = CompletedCharacter
			else:
				# Figures out if I don't need to do the chain because less then minumum days
				withinMin = 0
				for j in xrange(chain['minDays']):
					if (today - timedelta(days=i+j)).strftime('%Y-%m-%d') in chain['dates']:
						withinMin = 1
				
				withinMax = 0
				for k in xrange(chain['maxDays']):
					if (today - timedelta(days=i+k)).strftime('%Y-%m-%d') in chain['dates']:
						withinMax = 1

				if withinMin == 1:
					chainDisplay['data'][i] = NotRequiredCharacter
					if i == 0: chainComboAdd = 1
				elif withinMax == 1:
					chainDisplay['data'][i] = ShouldDoCharacter
					if i == 0: chainComboAdd = 1
				else:
					if(i == 0):
						chainDisplay['data'][i] = NeedToDoCharacter
					else:
						chainDisplay['data'][i] = SpacingCharacter

		# Get Chain length
		chainComboStart = testChainLength(today, chain, today)
		chainDisplay['length'] = str((today - chainComboStart).days + chainComboAdd)

		# Print Chain info
		printLine(chainDisplay, lengths)	


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
	print "Added new chain with id " + str(newChainId)

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



