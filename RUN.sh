#!/bin/bash

INTERFACE="wlx00c0cab9a65f"
CHANNEL=1

if iwconfig "$INTERFACE" | grep -q "Mode:Monitor"; then
    echo "$INTERFACE is in monitor mode."
else
    echo "$INTERFACE is NOT in monitor mode (e.g., it is in Managed mode)."
    sudo ip link set "$INTERFACE" down
    sudo iw dev "$INTERFACE" set type monitor
    sudo ip link set "$INTERFACE" up
    sudo iw dev "$INTERFACE" set channel $CHANNEL
fi

#change name based on the number of APs being used (single or multiple)
#sudo ~/Desktop/RSSI-Based-Localization/rssi_env/bin/python ~/Desktop/RSSI-Based-Localization/scripts/RSSIgather_single.py
