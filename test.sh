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
./chain.py add Test 5 6
./chain.py


# Mod
reset
printHeader "Mod 1"
./chain.py 1 mod "Changed 1" 5 6
./chain.py

reset
printHeader "Mod 2"
./chain.py 2 mod MORE 2 2
./chain.py


# Done
reset
printHeader "Done 1"
./chain.py 1 done
./chain.py

reset
printHeader "Done 1"
./chain.py 1 done 2015-03-08
./chain.py

reset
printHeader "Done 2"
./chain.py 2 done
./chain.py

