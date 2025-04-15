#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 09:23:04 2022

@author: didik
"""

from scapy.all import *
import itertools
import numpy as np
import random
import socket
import struct
import subprocess
import os
import glob
import pandas as pd

#%%

def sortappend(a,b):
    L=PacketList() 
    while True:
        if len(a) == 0 : 
            L = L + b 
            break 
        elif len(b) == 0: 
            L = L + a 
            break 
        if a[0].time < b[0].time: 
            L = L + a[:1] 
            a=a[1:] 
        elif a[0].time > b[0].time: 
            L = L + b[:1] 
            b=b[1:] 
        else: 
            L = L + a[:1] 
            L = L + b[:1] 
            a=a[1:] 
            b=b[1:]
    return PacketList(L)

def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def mergecap(filename1, filename2, folder_path):
    subprocess.Popen(['mergecap','-w', folder_path + 'merged.pcap', filename1, filename2])
    subprocess.Popen(['rm', filename1, filename2])
    
#%%

def extract_packet(data_dir, save_place, class_name, label):
    
    all_data_packet_df = pd.DataFrame()
    all_data_packet_np = []
    folder_path = data_dir

    os.chdir(folder_path)
    extension = 'pcap'
    
    full_data = []
    one_data = []
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    
    for fff in all_filenames:
        # print(fff)
        pkts = rdpcap(fff)
        s_pkts = pkts.sessions()

        del_keys = []
    
        for key in s_pkts.keys():
            if 'TCP' not in key:
                del_keys.append(key)
        for key in del_keys:
            s_pkts.__delitem__(key)
    
        # Sessions into flow, each flow is bidirectional and identified by 5-tuple
        
        f_pkts = []

        for i,j in itertools.combinations(s_pkts.keys(),2):
                
            if [p in j for p in i.split(' ')].count(False) == 0:
                
                aa = s_pkts[i]
                bb = s_pkts[j]
                pkt_count = 0
    
                for pkt in aa:
                    pkt_count +=1
                for pkt in bb:
                    pkt_count +=1
                
    
                if pkt_count >= 2050:
                    # print(fff)
                    filename1=folder_path+i+'.pcap'
                    filename2=folder_path+j+'.pcap'
                    wrpcap(filename1, aa)
                    wrpcap(filename2, bb)
                    # print("Big packet", i)
                    # print("Packet Size: %d" % pkt_count)
                    mergecap(filename1, filename2, folder_path)
                    time.sleep(10)
                    mergedfile = rdpcap(folder_path+'merged.pcap')
                    f_pkts.append(mergedfile)
                    subprocess.Popen(['rm', folder_path + 'merged.pcap'])
                # wrpcap(i+'foo.pcap', f_pkts)
                else:    
                    f_pkts.append(sortappend(s_pkts[i],s_pkts[j]))
                    
        del s_pkts
        del del_keys
        del pkts    
    
        # Processing flow data to input data
    
        data=[] 
        
        img_shape=(60,3) 
        for flow in f_pkts: 
            f = []
            for pkt in flow[:img_shape[1]]: 
                if(pkt.payload.name == 'ARP'):
                    #random IP
                    pkt.payload.psrc = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                    pkt.payload.pdst = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                elif(pkt.payload.name == 'IP'):
                    #random IP
                    pkt.payload.src = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                    pkt.payload.dst = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                #random MAC
                pkt.src = rand_mac()
                pkt.dst = rand_mac()
                #packet -> bytes
                pkt_50 = [field for field in raw(pkt)] 
                pkt_50.extend([0]*img_shape[0])
                f.extend(pkt_50[:img_shape[0]])
            #deal with pcaket<3
            if(img_shape[1]-len(flow) > 0):
                f.extend([0]*img_shape[0]*(img_shape[1]-len(flow)))
            data.append(f)
            data_packet = pd.DataFrame(data)
            # data_packet['filename'] = fff
            
        all_data_packet_np.append(data)
        all_data_packet_df = pd.concat([all_data_packet_df, data_packet], ignore_index = True)
    
    all_data_packet_df['label'] = label 
    
    
    dataset_dir = save_place + 'dataset/'
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        
    all_data_packet_df.reset_index(drop=True).to_csv(dataset_dir + class_name + ".csv")
    return all_data_packet_df
