from RSSIsystem import RSSI
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

                    collector.start_thread()

                if key.name == 'esc':

                    exit()
