#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:05:45 2022

@author: didik
"""

import threading
import os
import subprocess
from datetime import datetime
import pandas as pd
from io import StringIO
import sys
import os
import subprocess
from datetime import datetime

data = pd.read_csv("pods_ips.csv")
print(data)
sudoPassword = 'hsl1QAZ*&'
interfaces = ['cali94eb5288f9a', 'calie5258b0d9ac']

def Convert(string):
    li = list(string.split(" "))
    return li

timename = datetime.now().strftime("%Y%m%d-%H%M%S")

def recordtraffic(i):
    a = data.loc[i, "NAME"]
    print(a)
    b = Convert(a)

    command = './capture_tool.sh'.split()
    filename = timename+str(b)+'.pcap'
    cmd1 = subprocess.Popen(['echo',sudoPassword], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','-S', 'timeout', '20h'] + command + b, stdin=cmd1.stdout, stdout=subprocess.PIPE)
    
    
    #subprocess.Popen('sudo -S', shell=True,stdout=subprocess.PIPE)
    #subprocess.Popen(sudoPassword, shell=True,stdout=subprocess.PIPE)
    #subprocess.Popen(command1, shell=True,stdout=subprocess.PIPE)

    #output = cmd2.stdout.read.decode()
    #record = subprocess.call(["sudo ./capture_tool.sh 10.111.231.173"])

    #output = cmd2.stdout.read.decode()

for i in range(len(data)):
    threadProcess = threading.Thread(name='traffic', target=recordtraffic(i))
    threadProcess.daemon = True
    threadProcess.start()
    threadProcess.join()
