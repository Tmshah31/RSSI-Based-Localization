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
from rich import print as rprint 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.progress import track, Progress, TextColumn, BarColumn, TimeRemainingColumn, SpinnerColumn
from rich.layout import Layout
from rich.align import Align


console = Console()


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
                    self.average_signal_strength[i] = None
                    return
                total = sum(self.sig_strength[i])
                avg = total/len(self.sig_strength[i])

                self.average_signal_strength[i] = float(10 * np.log10(avg))
                
        print(self.average_signal_strength)
        return 
    
    def start_sniff(self):

        #clears the dictionaries from last run
        self.clear_dictionaries()
        sniff(iface=self.Wlan, prn=self.process_packet, store=0, timeout = 5)
        
        self.average_values()


    def start_thread(self):
        self.thread = threading.Thread(target=self.start_sniff)
        self.thread.start()



    def Monitor_Mode(self):

        result = subprocess.getoutput(["iwconfig", self.Wlan])

        time.sleep(1)

        if "Mode:Monitor" in result:
            rprint(Panel(f"{self.Wlan} is in Monitor Mode\nPress Enter to Continue..."))
            while True:
                event = keyboard.read_event(suppress=True)
                if event.name == "enter":
                    console.clear()
                    return
                elif event.name == "esc":
                    console.clear()
                    exit()
                else:
                    rprint("Key Not Recognized...")
        

        tasks = [
            (["sudo", "ip", "link", "set", self.Wlan, "down"]),
            (["sudo", "iw", "dev", self.Wlan, "set", "type", "monitor"]),
            (["sudo", "ip", "link", "set", self.Wlan, "up"])
        ]

        
        
        rprint(Panel(f"{self.Wlan} is NOT in Monitor Mode"))
        for command in track(tasks, description="Configuring Interface"):
            subprocess.run(command, capture_output=True)
            time.sleep(1)

        result = subprocess.getoutput(["iwconfig", self.Wlan])
        if "Mode:Monitor" in result:
            rprint(Panel(f"{self.Wlan} is in Monitor Mode\nPress Enter to Continue..."))
            while True:
                event = keyboard.read_event(suppress=True)
                if event.name == "enter":
                    console.clear()
                    return
                elif event.name == "esc":
                    console.clear()
                    exit() 
                else:
                    rprint("Key Not Recognized...")
            
        return 
    
    











        




