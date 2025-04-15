#!/bin/bash

#this scrip perform subdirectory check on the target system
# to use it just "./02_attack_reproduction_directorybrute.sh target_ip target_port"
n=0

while [ $n -lt 11 ];
do

        #echo "Normal Ping"
        #timeout 1m hping3 -S -p $2 $1

        echo "get directory list"
        dirb 'http://'$1':'$2

        n=$(( $n+1 ))

done
