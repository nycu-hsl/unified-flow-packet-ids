#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:34:37 2022

@author: didik
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
import gc
import datetime;
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
from tensorflow.keras.models import load_model

from pickle import load
import joblib
tf.get_logger().setLevel('ERROR')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from detection.extract_flow import extract_flow

#%%
# load model
savedModel=load_model('detection/cnn_nov_23rd.h5')
# savedModel.summary()


def flow_detection(filename):
    
    df, src_ip, dst_ip = extract_flow(filename)
    df = np.array(df).reshape(df.shape[0], df.shape[1], 1)
    prob_range = savedModel.predict(df, verbose=0)
    
    del df
    gc.collect()
    return prob_range, src_ip, dst_ip
    