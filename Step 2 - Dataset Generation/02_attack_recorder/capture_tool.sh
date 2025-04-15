#!/bin/bash


ip=$1
today=$(date +"%Y%m%d")
times=$(date +"%H%M")

./packet_capture -s $ip -d $ip -o "Result-$today-$times-$ip.pcap"

