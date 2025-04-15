#!/bin/python

import subprocess
import sys
import os
import pexpect
#import libtmux

class attack_seq:
    def __init__(self):
        attack_status = None
        google_frontend_ip = None
        google_frontend_port = 80
        dvwa_frontend_ip = None
        dvwa_frontend_port = 80
        load_generator_status = None

    def record_ip(self):
        subprocess.run()


    def record_iface(self):
        print()    
    
    def vulnerability_scan(self):
        print()

    def brute_force(self):
        print()

    def check_loadgenerator(self):
        kubeload = subprocess.run(['kubectl', 'get', 'deployments', 'loadgenerator'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = {}
        for row in kubeload.stdout.readline():
            




if __name__ == "__main__":
    a = attack_seq()

    result = a.check_loadgenerator
    print(result)

    if a.check_loadgenerator() == True:
        print("true")
    else:
        print("false")




