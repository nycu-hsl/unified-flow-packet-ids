#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:21:43 2022

@author: didik
"""

import time
import pathlib
import os
import gc
import numpy as np
from os import system, name 
from typing import Union

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent

from detection.extract_flow import extract_flow
from detection.flow_based import flow_detection
from detection.packet_based import packet_detection

import shutil

td_min = 0.409134
td_max = 0.51201195
te_min = 0.5120123
te_max = 0.975767
threshold_flow = 0.512012
threshold_packet = 0.536843


class CustomHandler(FileSystemEventHandler):
    """Custom handler for Watchdog"""

    def __init__(self):
        # List to store path
        self.path_strings = []

    # callback for File/Directory created event, called by Observer.
    def on_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]):
        # print(f"Event type: {event.event_type}\nAt: {event.src_path}")

        # check if it's File creation, not Directory creation
        if isinstance(event, FileCreatedEvent):
            
            # if so, do something with event.src_path - it's path of the created file.
            self.path_strings.append(event.src_path)
            #time.sleep(0.1)
            
            prob_flow, src_ip, dst_ip = flow_detection(event.src_path)
            # print(prob_flow)
            if td_min <= prob_flow <= td_max:
                detection_result = packet_detection(event.src_path, threshold_packet)
                if detection_result == 1:
                    print('Attack!!', 'source:', src_ip, 'destination:', dst_ip, 'by Packet Based')
                    # shutil.copy2(event.src_path, '/home/hsl/itri/live_detection/re_train_packet/')
            elif te_min <= prob_flow <= te_max:
                detection_result = packet_detection(event.src_path, threshold_packet)
                if detection_result == 1:
                    print('Attack!!', 'source:', src_ip, 'destination:', dst_ip, 'by Packet Based')
                    # shutil.copy2(event.src_path, '/home/hsl/itri/live_detection/re_train_packet/')
            else:
                detection_result = np.where(prob_flow < threshold_flow, 0, 1)
                if detection_result == 1:
                    print('Attack!!', 'source:', src_ip, 'destination:', dst_ip, 'by Flow Based')
                    # shutil.copy2(event.src_path, '/home/hsl/itri/live_detection/re_train/')
                    
            os.remove(event.src_path)
            self.path_strings.remove(event.src_path)
            
            del detection_result
            # del path_strings
            # del event.src_path
            del prob_flow
            gc.collect()

def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 
        
def main():

    clear()
    # get current path as absolute, linux-style path.
    print("Welcome to Hybrid Flow-and-Packet Anomaly Detection")
    working_path = (input("Input your traffic folder: "))
    
    #working_path = 'sniffer_data/'

    # create instance of observer and CustomHandler
    observer = Observer()
    handler = CustomHandler()
    print("Start the anomaly detection")

    # start observer, checks files recursively
    observer.schedule(handler, path=working_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
