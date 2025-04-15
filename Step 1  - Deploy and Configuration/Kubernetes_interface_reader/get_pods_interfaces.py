#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 06:48:36 2022

@author: didik
"""

import pandas as pd
from io import StringIO
import sys
import os
import subprocess
from datetime import datetime

data = pd.read_csv("pods.csv")
pods = data.values.tolist()
sudoPassword = 'hsl1QAZ*&'
sample_list = ['Python', 'with', 'FavTutor']
df = pd.DataFrame()

iface_name = pd.DataFrame([])


def Convert(string):
    li = list(string.split(" "))
    return li

for i in range(len(data)):
    a = data.loc[i, "NAME"]
    print(a)
    b = Convert(a)
    command = './interface_reader.sh'.split()
    cmd1 = subprocess.Popen(['echo',sudoPassword], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','-S'] + command + b, stdin=cmd1.stdout, stdout=subprocess.PIPE)
    result = cmd2.communicate("b\n")[0]
    result = result.decode().splitlines()
    print('iface_name: ', result)
    
    #iface_name = iface_name.append(pd.DataFrame({'pods_name': a, 'iface': result}, index=[0]))
    iface_name = pd.concat([iface_name, pd.DataFrame.from_records([{'pods_name': a, 'iface': result}])])

print(iface_name)
iface_name.to_csv("pods_iface.csv")
#print(df)


