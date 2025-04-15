#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 07:17:17 2022

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
from preprocessing.preprocessing_flow import extract_flow
from preprocessing.preprocessing_packet import extract_packet
from training.flow_training import start_flow_training
from training.packet_training import start_packet_training

matplotlib.use('Agg')
matplotlib.use('TkAgg')
# from classifier.train import train_main
# from classifier.adv_train import adv_train
# from attacker.attack import attack_test_main
# from attacker.attack import attack_train_main
# from evaluation.evaluation import evaluation
# from prediction_model.model_prediction import model_prediction
# from ensemble_creation.ensemble_basic import main_ensemble
import sys

"""
GLOBAL VARIABLE
"""

def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 

def select_dataset():
    clear()
    print("Select type of dataset:")
    print("1. Training")
    print("2. Testing")
    
    dataset =input("YOUR INPUT: ")
    return dataset
    

    
def select_location(data_type):
    # clear()
    if data_type == 1:
        pp = "BENIGN"
    elif data_type == 2:
        pp = "BRUTE FORCE TO DVWA PODS"
    elif data_type == 3:
        pp = "BRUTE FORCE TO E-COMMERCE APPS"
    elif data_type == 4:
        pp = "DOS ATTACK TO E-COMMERCE APPS"
    elif data_type == 5:
        pp = "SCANNING ATTACK TO DVWA PODS"
    elif data_type == 6:
        pp = "SCANNING ATTACK TO E-COMMERCE APPS"
    elif data_type == 7:
        pp = "SQL INJECTION"     
    elif data_type == 8:
        pp = "XSS ATTACK"     
   
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
    print("Welcome to Training System\n")
    print("Please choose one of the features below:")
    print("1. Train the flow-based detection")
    print("2. Train the packet-based detection")

    
    menu = int(input("YOUR INPUT: "))
    if menu == 1:
        
        mode = "FLow-Based"
        root_dir = os.getcwd()
        save_place = root_dir + '/flow/training_result/'
        if not os.path.exists(save_place):
            os.makedirs(save_place)
            
            
        print("Copy and paste the location of your PCAP data")
        benign_data = select_location(1)
        brute_dvwa = select_location(2)
        brute_google = select_location(3)
        dos_google = select_location(4)
        scanning_dvwa = select_location(5)
        scanning_google = select_location(6)
        sqli = select_location(7)
        xss = select_location(8)
        


        clear()
        
        print("------------- TRAINING DETAIL -------------")
        print("Training Results Location: " + save_place)
        print("Mode: " + mode)
        print("Save the dataset, CNN model, and scaler to that folder")
        print("------------------------------------------------")
        
        print("Start Preprocessing...")
        benign_train = extract_flow(benign_data, save_place, 'flow_benign', 0)
        brute_dvwa_train = extract_flow(brute_dvwa, save_place, 'flow_brute_dvwa', 1)
        brute_google_train = extract_flow(brute_google, save_place, 'flow_brute_google', 1)
        dos_google_train = extract_flow(dos_google, save_place, 'flow_dos_google', 1)
        scanning_dvwa_train = extract_flow(scanning_dvwa, save_place, 'flow_scanning_dvwa', 1)
        scanning_google_train = extract_flow(scanning_google, save_place, 'flow_scanning_google', 1)
        sqli_train = extract_flow(sqli, save_place, 'flow_sqli', 1)
        xss_train = extract_flow(xss, save_place, 'flow_xss', 1)
        
        train_data = pd.concat([benign_train, brute_dvwa_train, brute_google_train, dos_google_train, scanning_dvwa_train, scanning_google_train, sqli_train, xss_train])
        print("Start Training...")
        
        start_flow_training(train_data, save_place)
        
        print("FLOW-BASED TRAINING IS DONE")
        return 0
    
    elif menu == 2:
        
        mode = "Packet-Based"
        root_dir = os.getcwd()
        save_place = root_dir + '/packet/training_result/'
        if not os.path.exists(save_place):
            os.makedirs(save_place)
            
            
        benign_data = select_location(1)
        brute_dvwa = select_location(2)
        brute_google = select_location(3)
        dos_google = select_location(4)
        scanning_dvwa = select_location(5)
        scanning_google = select_location(6)
        sqli = select_location(7)
        xss = select_location(8)

        clear()
                
        print("------------- TRAINING DETAIL -------------")
        print("Training Results Location: " + save_place)
        print("Mode: " + mode)
        print("Save the dataset, CNN model, and scaler to that folder")
        print("------------------------------------------------")
        
        print("Start Preprocessing...")
        benign_train = extract_packet(benign_data, save_place, 'packet_benign', 0)
        brute_dvwa_train = extract_packet(brute_dvwa, save_place, 'packet_brute_dvwa', 1)
        brute_google_train = extract_packet(brute_google, save_place, 'packet_brute_google', 1)
        dos_google_train = extract_packet(dos_google, save_place, 'packet_dos_google', 1)
        scanning_dvwa_train = extract_packet(scanning_dvwa, save_place, 'packet_scanning_dvwa', 1)
        scanning_google_train = extract_packet(scanning_google, save_place, 'packet_scanning_google', 1)
        sqli_train = extract_packet(sqli, save_place, 'packet_sqli', 1)
        xss_train = extract_packet(xss, save_place, 'packet_xss', 1)
        
        train_data = pd.concat([benign_train, brute_dvwa_train, brute_google_train, dos_google_train, scanning_dvwa_train, scanning_google_train, sqli_train, xss_train])
        
        print("Start Training...")
        start_packet_training(train_data, save_place)
        
        print("PACKET-BASED TRAINING IS DONE")
        return 0
    

if __name__ == '__main__':
    main(sys.argv)