#!/bin/bash

#how to use "./interface_reader.sh pod_name"

get_container_id=$(docker ps |grep $1 |head -n 1|cut -d " " -f 1)

get_container_pid=$(docker inspect --format '{{ .State.Pid }}' $get_container_id)

get_number=$(nsenter -t $get_container_pid -n ip address | grep eth0|cut -d "@" -f 2 |head -n 1 |cut -d ":" -f 1 |cut -d "f" -f 2)

get_iface=$(ip -o address show|grep "$get_number:"|cut -d " " -f 2)
echo $get_iface


