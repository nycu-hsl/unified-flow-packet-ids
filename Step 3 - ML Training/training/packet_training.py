#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 15:12:25 2022

@author: didik
"""
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from tensorflow.keras.layers import Flatten, Dense, Conv1D, MaxPool1D, Dropout
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

import util.common as util

#%%

def start_packet_training(training_data, save_place):
        
    X = training_data.drop(columns = ['label']).copy()
    y = training_data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify=y, random_state=42)
    

    #Reshape train and test data to (n_samples, 187, 1), where each sample is of size (187, 1)
    X_train = np.array(X_train).reshape(X_train.shape[0], X_train.shape[1], 1)/255
    X_test = np.array(X_test).reshape(X_test.shape[0], X_test.shape[1], 1)/255

    # Create sequential model 
    cnn_model = tf.keras.models.Sequential()
    
    #First CNN layer  with 32 filters, conv window 3, relu activation and same padding
    cnn_model.add(Conv1D(filters=32, kernel_size=(3,), padding='same', activation=tf.keras.layers.LeakyReLU(alpha=0.001), input_shape = (X_train.shape[1],1)))
    
    #Second CNN layer  with 64 filters, conv window 3, relu activation and same padding
    cnn_model.add(Conv1D(filters=64, kernel_size=(3,), padding='same', activation=tf.keras.layers.LeakyReLU(alpha=0.001)))
    
    #Third CNN layer with 128 filters, conv window 3, relu activation and same padding
    cnn_model.add(Conv1D(filters=128, kernel_size=(3,), padding='same', activation=tf.keras.layers.LeakyReLU(alpha=0.001)))
    
    #Fourth CNN layer with Max pooling
    cnn_model.add(MaxPool1D(pool_size=(3,), strides=2, padding='same'))
    cnn_model.add(Dropout(0.5))
    
    #Flatten the output
    cnn_model.add(Flatten())
    
    #Add a dense layer with 256 neurons
    cnn_model.add(Dense(units = 256, activation=tf.keras.layers.LeakyReLU(alpha=0.001)))
    
    #Add a dense layer with 512 neurons
    cnn_model.add(Dense(units = 512, activation=tf.keras.layers.LeakyReLU(alpha=0.001)))
    
    #Softmax as last layer with five outputs
    cnn_model.add(Dense(units = 1, activation='sigmoid'))
    
    cnn_model.compile(optimizer='adam', loss = 'binary_crossentropy', metrics=['accuracy'])
    cnn_model.summary()
    cnn_model_history = cnn_model.fit(X_train, y_train, epochs=10, batch_size = 10, validation_data = (X_test, y_test))
    
    # plt.plot(cnn_model_history.history['accuracy'])
    # plt.plot(cnn_model_history.history['val_accuracy'])
    # plt.legend(["accuracy","val_accuracy"])
    # plt.title('Accuracy Vs Val_Accuracy')
    # plt.xlabel('Epoch')
    # plt.ylabel('Accuracy')
    
    #%% SAVED THE CNN MODEL
    cnn_model.save(save_place + 'cnn_packet_model.h5')

    #%%
    # joblib.dump(scaler, save_place + 'flow_scaler.gz')
    
    y_pred2 = cnn_model.predict(X_test)

    curves_metrics, summary_metrics = util.evaluate_proba(y_test, y_pred2)
    summary_metrics.to_csv(save_place + 'Summary_of_Thresholds_for_Packet_Detection.csv')
    print('Best Threshold for Packet Detection: ', summary_metrics.iat[0,2])
    
    threshold_b = summary_metrics.iat[0,2]
    y_pred_1 = np.where(y_pred2 < threshold_b, 0, 1)
    fig = util.plot_confusion_matrix(y_test, y_pred_1, values=[0, 1], labels=["Benign", "Fraud"])
    # fig.savefig(save_place + 'test_after_packet_training.png')