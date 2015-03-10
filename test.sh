#!/bin/bash

bold=`tput bold`
normal=`tput sgr0`


function reset {
	echo ''
	cp data.json.bak data.json
}

function printHeader() {	
	echo "${bold}$1${normal}"
}


# Print
reset
printHeader "Print"
./chain.py


# Delete
reset
printHeader "Delete 1"
./chain.py 1 delete
./chain.py

reset
printHeader "Delete 2"
./chain.py 2 delete
./chain.py

reset
printHeader "Delete 3"
./chain.py 3 delete
./chain.py


# Add
reset
printHeader "Add 3"
./chain.py add name min:5 max:6
./chain.py



