#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 21:23:16 2022

@author: hsl
"""
    
import numpy
from nfstream import NFPlugin, NFStreamer
import os
import pandas as pd
import shutil
import numpy as np
import pathlib
import pickle
import glob  
import joblib
import datetime;
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Flatten, Dense, Conv1D, MaxPool1D, Dropout
from pickle import load
import joblib
tf.get_logger().setLevel('ERROR')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


import threading
import subprocess
from datetime import datetime
from io import StringIO
import sys
import os
import subprocess
from getpass import getpass

#%%

data = pd.read_csv("sniffer/pods.csv")

    
def Convert(string):
    li = list(string.split(" "))
    return li        

def live_traffic(i, password):
    a = data.loc[i, "NAME"]
    b = Convert(a)
    
    command = 'sniffer/sniffer.py -i'.split()
    cmd1 = subprocess.Popen(['echo',password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','python3'] + command + b, stdin=cmd1.stdout, stdout=subprocess.PIPE)
    
#%%         
threads = []
def main():
  print('It requires to be ran in the sudo mode')
  password = getpass(prompt='Input your sudo password: ')  
  for i in range(len(data)):
     t = threading.Thread(target=live_traffic, args=(i, password,))
     threads.append(t)
     t.start()

  # block until all the threads finish (i.e. until all function_a functions finish)    
  for t in threads:
     t.join()
     
if __name__ =="__main__":
    main()
