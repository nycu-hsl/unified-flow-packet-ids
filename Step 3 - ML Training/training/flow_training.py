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
import matplotlib
# import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import util.common as util


import os

#%%

def start_flow_training(training_data, save_place):
        
    X = training_data.drop(columns = ['label']).copy()
    y = training_data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =0.2, stratify=y, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    X_train = np.array(X_train).reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = np.array(X_test).reshape(X_test.shape[0], X_test.shape[1], 1)

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
    cnn_model_history = cnn_model.fit(X_train, y_train, epochs=1, batch_size = 10, validation_data = (X_test, y_test))
    
    # plt.plot(cnn_model_history.history['accuracy'])
    # plt.plot(cnn_model_history.history['val_accuracy'])
    # plt.legend(["accuracy","val_accuracy"])
    # plt.title('Accuracy Vs Val_Accuracy')
    # plt.xlabel('Epoch')
    # plt.ylabel('Accuracy')
    
    #%% SAVED THE CNN MODEL
    cnn_model.save(f'{save_place}' + 'cnn_flow_model.h5')

    #%%
    joblib.dump(scaler, f'{save_place}' + 'flow_scaler.gz')
    
    y_pred2 = cnn_model.predict(X_test)

    curves_metrics, summary_metrics = util.evaluate_proba(y_test, y_pred2)
    summary_metrics.to_csv(save_place + 'Summary_of_Thresholds_for_Detection.csv')
    print('Best Threshold for Flow Detection: ', summary_metrics.iat[0,2])
    
    threshold_b = summary_metrics.iat[0,2]
    y_pred_1 = np.where(y_pred2 < threshold_b, 0, 1)
    fig = util.plot_confusion_matrix(y_test, y_pred_1, values=[0, 1], labels=["Benign", "Fraud"])
    # matplotlib.use('TkAgg')
    # matplotlib.use('Agg')
    # fig.show()
    # fig.savefig(f'{save_place}' + 'confusion_matrix_flow_test_after_training.png')

def main():
    benign_train = pd.read_feather('/home/didik/code/ead/aug_1/flow/benign.feather')
    brute_dvwa_train = pd.read_feather('/home/didik/code/ead/aug_1/flow/brute_dvwa.feather')
    train_data = pd.concat([benign_train, brute_dvwa_train])
    
    save_place = 'flow/training_result/'
    if not os.path.exists(save_place):
        os.makedirs(save_place)
        
    start_flow_training(train_data, save_place)
    
if __name__ == '__main__':
    main()
