#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:53:51 2022

@author: didik
"""

import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
# tf.compat.v1.disable_eager_execution()
# if tf.__version__[0] != '2':
#     raise ImportError('This notebook requires TensorFlow v2.')
# physical_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

import os
from os import system, name 
import pandas as pd
import matplotlib
from detection.preprocessing_flow import extract_flow
from detection.detection_flow import start_detection
from greyzone.findProbability import start_finding_greyzone_threshold

import sys

"""
GLOBAL VARIABLE
"""

def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 

    
def select_location(data_type):
    # clear()
    if data_type == 1:
        pp = "BENIGN"
    elif data_type == 2:
        pp = "ATTACK"
   
    return(input("YOUR " + pp +" FOLDER LOCATION: "))


def model_location():
    clear()
    print("Copy and paste your model location for testing:")
    return(input("YOUR MODEL LOCATION: "))



def main(argv):
    if len(argv) == 2:
        if argv[1] == "1":
            physical_devices = tf.config.list_physical_devices('GPU')
            tf.config.experimental.set_memory_growth(physical_devices[0], True)
    
    clear()
    print("Welcome to Greyzone Definition\n")
    print("This system is used to find the threshold for greyzone setting")
    print("You have to input some configurations to run the system ")

    root_dir = os.getcwd()
    save_place = root_dir + '/greyzone_threshold_results/'
    if not os.path.exists(save_place):
        os.makedirs(save_place)
        
        
    print("Input the PCAP files of your testing data")
    benign_data = select_location(1)
    attack_data = select_location(2)
    
    threshold_flow = input("Input the detection threshold of your flow-based: ")
    clear()
    
    print("------------- GREYZONE DETAIL -------------")
    print("Greyzone Threshold Results: " + save_place)
    print("------------------------------------------------")
    
    print("Start Preprocessing...")
    benign_testing = extract_flow(benign_data, save_place, 'flow_benign', 0)
    attack_testing = extract_flow(attack_data, save_place, 'flow_attack', 1)
    
    testing_data = pd.concat([benign_testing, attack_testing])
    print("Start Testing...")
    
    data_for_greyzone = start_detection(testing_data, threshold_flow)
    start_finding_greyzone_threshold(data_for_greyzone, save_place)
    
    print("Finish...")
    print("Check " + save_place + " to see the detail results")
    return 0
    

if __name__ == '__main__':
    main(sys.argv)