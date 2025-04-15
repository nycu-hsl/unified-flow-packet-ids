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
import datetime;
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
from tensorflow.keras.models import load_model

from pickle import load
import joblib
tf.get_logger().setLevel('ERROR')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from detection.preprocessing_flow import extract_flow


#%%
# load model
savedModel=load_model('detection/cnn_flow_model.h5')
scaler = joblib.load('detection/cnn_flow_scaler.gz')

# savedModel.summary()


def start_detection(filename, threshold_flow):
    
    X = filename.drop(columns = ['label']).copy()
    y = filename['label']
    
    X = scaler.transform(X)
    X = np.array(X).reshape(X.shape[0], X.shape[1], 1)
    prob_range = savedModel.predict(X, verbose=0)
    
    detection_result = np.where(prob_range <= float(threshold_flow), 0, 1)
    
    y_test2 = y.to_numpy()
    y_pred_inv = pd.DataFrame(detection_result)
    y_test_inv = pd.DataFrame(y_test2)
    x_pred_inv = pd.DataFrame(prob_range)
    y_test_inv.rename(columns={0: 'label'}, inplace=True)
    y_pred_inv.rename(columns={0: 'detection_results'}, inplace=True)
    x_pred_inv.rename(columns={0: 'detection_probability'}, inplace=True)
    
    yyy = pd.concat([y_test_inv, y_pred_inv, x_pred_inv], axis=1, join='inner')
    
    return yyy
    