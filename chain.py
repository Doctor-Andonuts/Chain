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
	BOLD = '\033[1m'
	END = '\033[0m'
	DARK_GREEN = '\033[48;5;22m'
	LIGHT_GREEN = '\033[48;5;2m'
	RED = '\033[48;5;88m'
	YELLOW = '\033[48;5;226m'
	BLUE = '\033[48;5;20m'

today = datetime.now()

TEST = 0
if TEST:
	testFileNameAdd = '.test'
	print color.BOLD + "\nTEST DATA\n" + color.END
else:
	testFileNameAdd = ''



# Configuration
CompletedCharacter = color.LIGHT_GREEN + "  " + color.END
NotRequiredCharacter = color.DARK_GREEN + "  " + color.END
ShouldDoCharacter = color.YELLOW + "  " + color.END
NeedToDoCharacter = color.RED + "  " + color.END
SpacingCharacter = " "
NotCountCharacter = color.BLUE + "  " + color.END
daysToShow = 7
chainDataFileName = '/.chain.json' + testFileNameAdd
homedir = os.path.expanduser('~')



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
	loopRange = chain['maxDays']
	i = 0
#	for i in xrange(1, loopRange):
	while i < loopRange:
		i += 1
		testDate = checkDate - timedelta(days = i)
		testDateString = testDate.strftime('%Y-%m-%d')
		if testDateString in chain['dates'] and (chain['dates'][testDateString] == 'S' or chain['dates'][testDateString] == 'V' or chain['dates'][testDateString] == 'O'):
			loopRange += 1
		elif testDateString in chain['dates'] and chain['dates'][testDateString] == 'X':
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
				if chain['dates'][dateTest] == 'X':
					chainDisplay['data'][i] = CompletedCharacter
				else:
					chainDisplay['data'][i] = NotCountCharacter
				if i == 0: chainComboAdd = 1
			else:
				# Figures out if I don't need to do the chain because less then minumum days
				withinMin = 0
				for j in xrange(chain['minDays']):
					if (today - timedelta(days=i+j)).strftime('%Y-%m-%d') in chain['dates']:
						if chain['dates'][(today - timedelta(days=i+j)).strftime('%Y-%m-%d')] == 'X':
							withinMin = 1
				
				withinMax = 0
				chainDaysToTest = chain['maxDays']
				counter = 0
				while counter < chainDaysToTest:
					dateTestMax = (today - timedelta(days=i+counter)).strftime('%Y-%m-%d')
					if dateTestMax in chain['dates']:
						if chain['dates'][dateTestMax] == 'X':
							withinMax = 1
						elif chain['dates'][dateTestMax] == 'S' or chain['dates'][dateTestMax] == 'V' or chain['dates'][dateTestMax] == 'O':
							chainDaysToTest += 1
					counter += 1

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
	newDates = {}
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
			

def markChainDone(filterId, doneDate, chainDoneType):
	for chain in Chains:
		if int(filterId) == int(chain['id']):
			chain['dates'][doneDate] = chainDoneType
			

#---------------------------


# Load json chain data from the datafile
with open(homedir + chainDataFileName, 'a+') as JsonFile: # This creates a new file if one did not exist
	try:
		Chains = json.load(JsonFile)
	except ValueError, e:
		Chains = []


# Chains = list
# Chains[0] = dict
# Chains[0]['names'] = unicode
# Chains[0]['maxDays'] = unicode
# Chains[0]['minDays'] = unicode
# Chains[0]['dates'] = dict
# Chains[0]['dates']['<date>'] = <code> (code is X,S,V, or O for Compelted, Sick, Vacation, or Offday)



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
	elif sys.argv[2] == 'sick':
		if len(sys.argv) <= 3:
			doneDate = today.strftime("%Y-%m-%d")
		else:
			doneDate = sys.argv[3]
		markChainDone(sys.argv[1], doneDate, 'S')
	elif sys.argv[2] == 'vacation':
		if len(sys.argv) <= 3:
			doneDate = today.strftime("%Y-%m-%d")
		else:
			doneDate = sys.argv[3]
		markChainDone(sys.argv[1], doneDate, 'V')
	elif sys.argv[2] == 'offday':
		if len(sys.argv) <= 3:
			doneDate = today.strftime("%Y-%m-%d")
		else:
			doneDate = sys.argv[3]
		markChainDone(sys.argv[1], doneDate, 'O')
	elif sys.argv[2] == 'done':
		if len(sys.argv) <= 3:
			doneDate = today.strftime("%Y-%m-%d")
		else:
			doneDate = sys.argv[3]
		markChainDone(sys.argv[1], doneDate, 'X')
	else:
		print 'Syntax Error'


# Write my new JSON to file
with open(homedir + chainDataFileName, 'w') as outfile:
	json.dump(Chains, outfile)



