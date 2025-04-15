#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 06:34:59 2022

@author: didik
"""

import os
from nfstream import NFStreamer, NFPlugin
import pandas as pd
import numpy as np
import glob  
import joblib
import gc

#%%

scaler = joblib.load('detection/cnn_nov_23rd_scaler.gz')

remove_parameter = [
  'id',
  'expiration_id',
  'src_ip',
  'src_mac',
  'src_oui',
  'src_port',
  'dst_oui',
  'dst_port',
  'dst_ip',
  'dst_mac',
  'dst_mac',
  'ip_version',
  'vlan_id',
  'tunnel_id',
  'application_name',
  'application_category_name',
  'application_is_guessed',
  'application_confidence',
  'requested_server_name',
  'client_fingerprint',
  'server_fingerprint',
  'user_agent',
  'content_type',
  'Unnamed: 0',
  'index',
  'bidirectional_first_seen_ms',
  'bidirectional_last_seen_ms',
  'src2dst_first_seen_ms',
  'src2dst_last_seen_ms',
  'dst2src_first_seen_ms',
  'dst2src_last_seen_ms'
]

def remove_param(df):
    for total_remove_parameter in range (0, len(remove_parameter)):
        for feature in range(0, len(df.columns)):
            if remove_parameter[total_remove_parameter] == df.columns[feature]:
                df = df.drop(columns=remove_parameter[total_remove_parameter])
                break
            
    return df

def remove_inf_nan(df):
    
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    #print(f"{df.isna().any(axis=1).sum()} invalid rows dropped")
    df.dropna(inplace=True)
    
    remove_rows_with_str = dict()
    
    
    return df

#%%
def extract_flow(filename):
    
    df = NFStreamer(source=filename, statistical_analysis=True, active_timeout=18000000000000000, idle_timeout=10000000000000000).to_pandas()
    src_ip = df['src_ip'].values[0]
    dst_ip = df['dst_ip'].values[0]
    df = remove_param(df)
    df = remove_inf_nan(df)
    df = scaler.transform(df)

    return df, src_ip, dst_ip
