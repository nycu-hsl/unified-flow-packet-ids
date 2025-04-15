#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:31:43 2022

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
import joblib
import gc
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
from tensorflow.keras.models import load_model

from pickle import load
import joblib
tf.get_logger().setLevel('ERROR')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
tf.config.run_functions_eagerly(True)
tf.data.experimental.enable_debug_mode()

#%%
savedModel=load_model('detection/cnn_ead_november_23_all_data.h5')
threshold_packet = 0.536843

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

def extract_packet(data_dir):
    
    folder_path = os.getcwd()
    
    pkts = rdpcap(data_dir)
    s_pkts = pkts.sessions()

    del_keys = []

    for key in s_pkts.keys():
        if 'TCP' not in key:
            del_keys.append(key)
    for key in del_keys:
        s_pkts.__delitem__(key)
    
    f_pkts = []
    f_pkts.append(pkts)
                
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
    
    del f_pkts
    del f
    gc.collect()
    
    return data_packet

def packet_detection(filename, threshold_packet):
    
    data_packet = extract_packet(filename)
    data_packet = np.array(data_packet).reshape(data_packet.shape[0], data_packet.shape[1], 1)/255

    try:
        prob_packet = savedModel.predict(data_packet, verbose=0)
        detection_result = np.where(prob_packet < threshold_packet, 0, 1)
        del data_packet
        
        gc.collect()
    except ValueError:
        detection_result = 0
        print('empty batch_outputs')
    return detection_result
