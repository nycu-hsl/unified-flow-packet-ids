#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:27:02 2022

@author: didik
"""
import subprocess
import os
import glob
import sys

# folder_path = "/home/didik/code/ead/pcap/vulnerability_social_media/rewrite/"
folder_path = sys.argv[1]
out_dir = sys.argv[2]

# out_dir = "/home/didik/code/ead/pcap/vulnerability_social_media/rewrite/result/"
os.chdir(folder_path)
extension = 'pcap'

def Convert(string):
    li = list(string.split(" "))
    return li


all_filenames = [i for i in glob.glob("*.{}".format(extension))]


for fff in all_filenames:
    
    print(fff)
    b = Convert(fff)
    infile = "--infile=" + fff
    outfile = "--outfile=" + out_dir + fff
    #command = 'tcprewrite --dlt=enet'.split()
    subprocess.run(['tcprewrite',
                '--dlt=enet',
                str(infile),
                str(outfile)],
                   stdout=subprocess.PIPE)