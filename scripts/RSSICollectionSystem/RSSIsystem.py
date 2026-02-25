from scapy.all import sniff, Dot11Beacon, RadioTap, Dot11
import os
import time
import keyboard
import numpy as np
import csv
from pathlib import Path
from datetime import datetime
import psutil
import threading
import subprocess


class RSSI:

    def __init__(self, filename, Wlan, beacon_number):
        self.filename = filename
        self.Wlan = Wlan

        self.X = 0
        self.Y = 0
        
        
        self.beacon_number = beacon_number
        self.beacon_count = {}   #count the numbers of beacons we collected (we can swap this out for timeout later)
        self.sig_strength = {}   #list of values collected
        self.average_signal_strength = {} #will be in dBm

        #threads
        self.lock = threading.Lock() #for our shared dictionaries
        self.thread = None
        
        
        

    def load_file(self):
        with open(self.filename, 'r') as f:
            for line in f: 
                key = line.strip()

                if key:
                    self.beacon_count[key] = 0
                    self.sig_strength[key] = []
                    self.average_signal_strength[key] = 0 #this is the final values after averaging and convering to dB


    def process_packet(self, packet):
        if(packet.haslayer(Dot11Beacon) and packet.haslayer(RadioTap)):
            bssid = packet.getlayer(Dot11).addr2

            

            if bssid.upper() in self.beacon_count:

                with self.lock:

                    sig_strength = packet[RadioTap].dBm_AntSignal

                    sig_linear = 10**(sig_strength/10)
                    self.sig_strength[bssid.upper()].append(sig_linear) #don't forget to clear the list  

                    self.beacon_count[bssid.upper()] += 1 #don't forget to reset to zero

        

    def stop_sniff(self, packet):
        return all(count == self.beacon_number for count in self.beacon_count.values())
    

    #call after a sniff has been performed at a given location
    def clear_dictionaries(self):

        with self.lock:

            for value in self.sig_strength.values():
                value.clear()

            for value in self.beacon_count:
                self.beacon_count[value] = 0
                

        return


    def average_values(self):

        with self.lock:

            for i in self.beacon_count:
                if len(self.sig_strength[i]) <= 0:
                    self.average_signal_strength = None
                total = sum(self.sig_strength[i])
                avg = total/len(self.sig_strength[i])

                self.average_signal_strength[i] = float(10 * np.log10(avg))

        return 
    
    def start_sniff(self):

        #clears the dictionaries from last run
        self.clear_dictionaries()
        sniff(iface=self.Wlan, prn=self.process_packet, store=0, filter="type mgt subtype beacon", stop_filter = self.stop_sniff, timeout = 5)



    def start_thread(self):
        self.thread = threading.Thread(target=self.start_sniff)
        self.thread.start()


    def Monitor_Mode(self):

        result = subprocess.getoutput(["iwconfig", self.Wlan], text=True)

        if "Mode:Monitor" in result:
            print(f"{self.Wlan} is in Monitor Mode")
            return
        else:
            print(f"{self.Wlan} is NOT in Monitor Mode")
            subprocess.run(["sudo", "ip", "link", "set", self.Wlan, "down"])
            time.sleep(1)
            subprocess.run(["sudo", "iw", "dev", self.Wlan, "set", "type", "monitor"])
            time.sleep(1)
            subprocess.run(["sudo", "ip", "link", "set", self.Wlan, "up"])
            time.sleep(1)

            result = subprocess.getoutput(["iwconfig", self.Wlan]).decode('utf-8')
            if "Mode:Monitor" in result:
                print(f"{self.Wlan} is in Monitor Mode")
                return
            
        return 











        




