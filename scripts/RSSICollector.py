from scapy.all import * 
import os
import time
import keyboard
import numpy as np
import csv
from pathlib import Path
from datetime import datetime
import psutil


class RSSI:

    def __init__(self, filename, Wlan, beaconNumber):
        self.filename = filename
        self.X = 0
        self.Y = 0
        self.beaconNumber = beaconNumber
        self.BeaconCount = {}
        self.SigStrength = {}
        self.AverageSignalStrength = {}
        self.Wlan = Wlan
        

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

                sig_strength = packet[RadioTap].dBm_AntSignal

                sig_linear = 10**(sig_strength/10)
                self.SigStrength[bssid.upper()].append(sig_linear) #don't forget to clear the list  

                self.BeaconCount[bssid.upper()] += 1 #don't forget to reset to zero

        

    def stop_sniff(self, packet):
        return all(count == self.beaconNumber for count in self.BeaconCount.values())
    

    #call after a sniff has been performed at a given location
    def clear_dictionaries(self):

        for value in self.SigStrength.values():
            value.clear()

        for value in self.BeaconCount:
            self.BeaconCount[value] = 0

        return


    def average_values(self):

        for i in self.BeaconCount:
            total = sum(self.SigStrength[i])
            avg = total/len(self.SigStrength[i])

            self.AverageSignalStrength[i] = 10 * np.log10(avg)

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


    cards = list_all_net_interfaces()

    for i in range(len(cards)):
        print(f"{i}:{cards[i]}")

    selected = int(input("Select the card for WIFI sniff:"))

    print(f"{cards[selected]} has been chosen for sniff")


    collector = RSSI("/home/tmshah/Desktop/RSSI-Based-Localization/MAC.txt", cards[selected], 5)

    collector.load_file()

    print(collector.BeaconCount)
    print(collector.SigStrength)


    sniff(iface=cards[selected], prn=collector.process_packet, store=0, filter="type mgt subtype beacon", stop_filter = collector.stop_sniff)

    print(collector.AverageSignalStrength)


    exit()



        




