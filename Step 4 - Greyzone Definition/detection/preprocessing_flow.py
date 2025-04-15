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


#%%

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
def extract_flow(data_dir, save_place, class_name, label):
    
    os.chdir(data_dir)

    extension = 'pcap'
    all_data = pd.DataFrame()
    
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    
    for f in all_filenames:
        # print(f)
        df = NFStreamer(source=f, statistical_analysis=True).to_pandas()
        df = remove_param(df)
        df = remove_inf_nan(df)
        df['label'] = label
        all_data = pd.concat([all_data,df], ignore_index=True)
        
    dataset_dir = save_place + 'testing_data/'
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
                
    all_data.reset_index(drop=True).to_feather(dataset_dir + class_name + ".feather")
    return all_data
