#!/bin/bash

bold=`tput bold`
normal=`tput sgr0`


function reset {
	echo ''
	cp ~/chain/test.json ~/.chain.json
}

function printHeader() {	
	echo "${bold}$1${normal}"
}


cp ~/.chain.json ~/.chain.json.bak

# Print
reset
printHeader "Print"
chain


# Delete
reset
printHeader "Delete 1"
chain 1 delete
chain

reset
printHeader "Delete 2"
chain 2 delete
chain

reset
printHeader "Delete 3"
chain 3 delete
chain


# Add
reset
printHeader "Add 3"
chain add Test 5 6
chain


# Mod
reset
printHeader "Mod 1"
chain 1 mod "Changed 1" 5 6
chain

reset
printHeader "Mod 2"
chain 2 mod MORE 2 2
chain


# Done
reset
printHeader "Done 1"
chain 1 done
chain

reset
printHeader "Done 1"
chain 1 done 2015-03-08
chain

reset
printHeader "Done 2"
chain 2 done
chain



cp ~/.chain.json.bak ~/.chain.json
