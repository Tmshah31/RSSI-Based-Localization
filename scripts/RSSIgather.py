from scapy.all import * 
import os
import time
import keyboard


APs = ["ESP_Beacon_one", "ESP_Beacon_two", "ESP_Beacon_three"]
flags = [0,0,0] #[RSSI_AP1 -> RSSI_AP3]
wlan = "wlx00c0cab9a65f"

def beacon_parse(packet):
    if(packet.haslayer(Dot11Beacon) and packet.haslayer(RadioTap)):
        ssid = packet[Dot11Elt].info.decode('utf-8')
        if(ssid == APs[0] and flags[0] == 0):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            flags[0] = 1
        elif(ssid == APs[1] and flags[1] == 0):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            flags[1] = 1
        elif(ssid == APs[2] and flags[2] == 0):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            flags[2] = 1 

        if(flags[0] == 1 and flags[1] == 1 and flags[2] == 1):
            print("Found all SSID beacons")
            return

#Start the WLAN in monitor mod 
def Monitor_mode():
    
    os.system(f"sudo ip link set {wlan} down")
    time.sleep(1)
    os.system(f"sudo iw dev {wlan} set type monitor")
    time.sleep(1)
    os.system(f"sudo ip link set {wlan} up")
    time.sleep(1)

    os.system(f"iwconfig {wlan}")


# def Coordinatesystem(key):


    
if __name__ == "__main__":

    #Monitor_mode()

    X = 0
    Y = 0

    while(True):
        key = keyboard.read_event(suppress=True)
        if key.event_type == keyboard.KEY_DOWN:
            if key.name == "up":
                Y += 1
                print(f"Y: {Y}")
            if key.name == "down":
                Y -= 1
                print(f"Y: {Y}")
            if key.name == "right":
                X += 1
                print(f"X: {X}")
            if key.name == "left":
                X -= 1
                print(f"X: {X}")
            if key.name == "enter":
                print(f"Starting sniff at ({X},{Y})")    

    #sniff(iface=wlan, prn=beacon_parse, store=0, filter="type mgt subtype beacon")
