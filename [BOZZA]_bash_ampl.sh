#! /bin/bash

NUM=0
while [  $NUM -lt 11 ]; do
        PERCENTAGE=100
        while [ $PERCENTAGE -gt 0 ]; do
        	command='/home/daniubo/Scaricati/ampl.linux64/ampl '
        	command+='lp_run_'
        	command+=$NUM
        	command+='_'
        	command+=$PERCENTAGE
        	command+='.run'
        	echo $command
        	$command
        	let PERCENTAGE=PERCENTAGE-10
        	done
        let NUM=NUM+1
        done 