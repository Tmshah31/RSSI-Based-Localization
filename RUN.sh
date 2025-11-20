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

sudo /home/tmshah/RSSI_Localization/RSSI-Based-Localization/rssi_env/bin/python /home/tmshah/RSSI_Localization/RSSI-Based-Localization/scripts/RSSIgather_mutliple.py