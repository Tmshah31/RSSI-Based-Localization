#!/bin/bash

stty -echoctl

#change name based on the number of APs being used (single or multiple)
sudo  /home/kali/Desktop/RSSI-Based-Localization/rssi_env/bin/python /home/kali/Desktop/RSSI-Based-Localization/scripts/RSSICollectionSystem/main.py /home/kali/Desktop/RSSI-Based-Localization/MAC.txt
