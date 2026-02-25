from scapy.all import * 
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

    def __init__(self, filename, Wlan, beaconNumber):
        self.filename = filename
        self.Wlan = Wlan

        self.X = 0
        self.Y = 0
        
        
        self.beaconNumber = beaconNumber
        self.BeaconCount = {}   #count the numbers of beacons we collected (we can swap this out for timeout later)
        self.SigStrength = {}   #list of values collected
        self.AverageSignalStrength = {} #will be in dBm

        #threads
        self.lock = threading.Lock() #for our shared dictionaries
        self.thread = None
        
        
        

    def load_file(self):
        with open(self.filename, 'r') as f:
            for line in f: 
                key = line.strip()

                if key:
                    self.BeaconCount[key] = 0
                    self.SigStrength[key] = []
                    self.AverageSignalStrength[key] = 0 #this is the final values after averaging and convering to dB


    def process_packet(self, packet):
        if(packet.haslayer(Dot11Beacon) and packet.haslayer(RadioTap)):
            bssid = packet.getlayer(Dot11).addr2

            

            if bssid.upper() in self.BeaconCount:

                with self.lock:

                    sig_strength = packet[RadioTap].dBm_AntSignal

                    sig_linear = 10**(sig_strength/10)
                    self.SigStrength[bssid.upper()].append(sig_linear) #don't forget to clear the list  

                    self.BeaconCount[bssid.upper()] += 1 #don't forget to reset to zero

        

    def stop_sniff(self, packet):
        return all(count == self.beaconNumber for count in self.BeaconCount.values())
    

    #call after a sniff has been performed at a given location
    def clear_dictionaries(self):

        with self.lock:

            for value in self.SigStrength.values():
                value.clear()

            for value in self.BeaconCount:
                self.BeaconCount[value] = 0

        return


    def average_values(self):

        with self.lock:

            for i in self.BeaconCount:
                total = sum(self.SigStrength[i])
                avg = total/len(self.SigStrength[i])

                self.AverageSignalStrength[i] = float(10 * np.log10(avg))

        return 
    
    def start_sniff(self):

        #clears the dictionaries from last run
        collector.clear_dictionaries()
        sniff(iface=self.Wlan, prn=collector.process_packet, store=0, filter="type mgt subtype beacon", stop_filter = collector.stop_sniff)



    def start_thread(self):
        self.thread = threading.Thread(target=self.start_sniff)
        self.thread.start()


    def Monitor_Mode(self):

        result = subprocess.getoutput(["iwconfig", self.Wlan]).decode('utf-8')

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




            






def list_all_net_interfaces():
    # Get all network interfaces
    interfaces = psutil.net_if_addrs()
    cards = []

    print("Available Network Cards:")
    for interface_name in interfaces:
        cards.append(interface_name)

    return cards



if __name__ == "__main__":

    modes = ["Manual", "Auto (GNSS)"]


    cards = list_all_net_interfaces()

    for i in range(len(cards)):
        print(f"{i}:{cards[i]}")

    selected = int(input("Select the card for WIFI sniff:"))

    print(f"{cards[selected]} has been chosen for sniff")


    collector = RSSI("/home/tmshah/Desktop/RSSI-Based-Localization/MAC.txt", cards[selected], 5)
    collector.load_file()

    print("Please select a Mode for operation: ")
    for i in range(len(modes)): 
        print(f"{i} : {modes[i]}")

    selected_mode = int(input("Mode: "))
    collector.Monitor_Mode()
    

    #Manual Mode
    if modes[selected_mode] == modes[0]:
        print("entered")
        while(True):
            key = keyboard.read_event(suppress=True)
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == "up":
                    collector.Y += 1
                    print(f"Y: {collector.Y}")
                if key.name == "down":
                    collector.Y -= 1
                    print(f"Y: {collector.Y}")
                if key.name == "right":
                    collector.X += 1
                    print(f"X: {collector.X}")
                if key.name == "left":
                    collector.X -= 1
                    print(f"X: {collector.X}")
                if key.name == "enter":

                    collector.average_values()

                    print(collector.AverageSignalStrength)

                if key.name == 'esc':

                    exit()



        




