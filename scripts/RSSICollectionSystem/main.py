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
from rich_menu import Menu
from rich import print as rprint 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live



def list_all_net_interfaces():
    # Get all network interfaces
    interfaces = psutil.net_if_addrs()
    cards = []

    print("Available Network Cards:")
    for interface_name in interfaces:
        cards.append(interface_name)

    return cards




def create_menu(options, selected):
    

    def render(options,selected):
        text = Text()
        for i, opt in enumerate(options):
            if i == selected:
                text.append(f">{opt}\n", style="bold magenta")
            else:
                text.append(f" {opt}\n")

        return Panel(text, title="Select WLAN Card")
    
    with Live(render(options, selected), refresh_per_second=10, screen=True) as live:
        while True:
            event = keyboard.read_event()
            if event.event_type != "down":
                continue

            if event.name == "up":
                selected = (selected - 1) % len(options)
            elif event.name == "down":
                selected = (selected + 1) % len(options)
            elif event.name == "enter":
                break

            live.update(render(options, selected))

        rprint(f"Selected Card: {options[selected]}")  

        return selected  


if __name__ == "__main__":

    modes = ["Manual", "Auto (GNSS)"]

    cards = list_all_net_interfaces()
    selected_card = 0

    # for i in range(len(cards)):
    #     print(f"{i}:{cards[i]}")

    # selected = int(input("Select the card for WIFI sniff:"))

    # print(f"{cards[selected]} has been chosen for sniff")

    selected_card = create_menu(cards, selected_card)


    collector = RSSI("/home/tshah/Desktop/RSSI-Based-Localization/MAC.txt", cards[selected_card], 5)
    collector.load_file()

    collector.Monitor_Mode()

    print("Please select a Mode for operation: ")
    for i in range(len(modes)): 
        print(f"{i} : {modes[i]}")

    selected_mode = int(input("Mode: "))
    
    

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
