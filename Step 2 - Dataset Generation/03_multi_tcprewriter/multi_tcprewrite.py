#!/bin/python
import os
import subprocess
import sys
import pexpect

class multi_tcprewrite:
    def __init__(self):
        print("init")

    def rewrite(self):
        input_folder = sys.argv[1]
        dir_content = os.listdir(input_folder)

        #check result directory
        path = input_folder + "Result/"
        output_dir = path
        if os.path.exists(path):
            for f in dir_content:
                filename = f.rsplit(".")
                new_filename = "rewrite_" + filename[0] + ".pcap"
                infile = "--infile=" + input_folder + f
                outfile = "--outfile=" + output_dir + new_filename
                print(infile)
                print(outfile)

                subprocess.run(['tcprewrite',
                                '--dlt=enet',
                                str(infile),
                                str(outfile)],
                               stdout=subprocess.PIPE)

        else:
            subprocess.run(['mkdir', input_folder+'/Result'], stdout=subprocess.PIPE)
            for f in dir_content:
                filename = f.rsplit(".")
                new_filename = "rewrite_" + filename[0] + ".pcap"
                infile = "--infile=" + input_folder + f
                outfile = "--outfile=" + output_dir + new_filename

                subprocess.run(['tcprewrite',
                                '--dlt=enet',
                                str(infile),
                                str(outfile)],
                               stdout=subprocess.PIPE)

if __name__ == "__main__":
    r = multi_tcprewrite()
    try:
        if os.path.isfile('/usr/bin/tcprewrite'):
            r.rewrite()
        else:
            print("Installing tcpreplay module")
            subprocess.run(['sudo', 'apt', 'install', 'tcpreplay'])
            r.rewrite()
    except SyntaxError:
        print("Run python multi_tcprewrite.py <input_folder> <output_folder>")