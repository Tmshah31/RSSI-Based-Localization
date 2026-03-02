#!/bin/bash

stty -echoctl

#change name based on the number of APs being used (single or multiple)
sudo  /home/cyber-pi/Desktop/RSSI-Based-Localization/rssi_env/bin/python /home/cyber-pi/Desktop/RSSI-Based-Localization/scripts/RSSICollectionSystem/main.py
