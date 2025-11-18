from scapy.all import * 
import os
import time
import keyboard
import numpy as np
import csv
from pathlib import Path
from datetime import datetime


APs = ["ESP_Beacon_one", "ESP_Beacon_two", "ESP_Beacon_three"]
#flags = [0,0,0] #[RSSI_AP1 -> RSSI_AP3]
BeaconCount = {
    "ESP_Beacon_one" : 0 ,
    "ESP_Beacon_two" : 0,
    "ESP_Beacon_three" : 0}
wlan = "wlx00c0cab9a65f"


#which esp will be tested
global selector

#global variables so they can be access from data write function
X = 0
Y = 0

#store the signal strength values -> make sure to convert into linear before adding them into the list 
#These arrays need to be cleared before the beacon_parse returns to get them ready for the next run 
ESP_1 = []



def write_dataset(AP):
    csv_header = ['SSID', "X", "Y", "RSSI (avg)"]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_name = Path("/home/tmshah") / "RSSI_Localization" / "RSSI-Based-Localization" / "data" / f"{APs[AP]}_{timestamp}_dataset.csv"

    csvfile = open(csv_name, 'w', newline='')

    csv_writer = csv.writer(csvfile)

    csv_writer.writerow(csv_header)

    return csvfile



def average_RSSI(values):
    total = sum(values)
    avg = total/len(values)
    return avg


def stop_sniff(packet):

    return (BeaconCount[APs[selector]] == 5)

def beacon_parse(packet):
    if(packet.haslayer(Dot11Beacon) and packet.haslayer(RadioTap)):
        ssid = packet[Dot11Elt].info.decode('utf-8')
        if(ssid == APs[selector] and BeaconCount[APs[selector]] < 5):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            sig_linear = 10**(sig_strength/10)
            ESP_1.append(sig_linear)
            BeaconCount[APs[selector]] += 1 

        if(BeaconCount[APs[selector]] == 5):
            print("Found all SSID beacons")


            

            



#Start the WLAN in monitor mode -> might be better to move this into the run.sh bash script
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

    selector = int(input("Select ESP:\n0:ESP1\n1:ESP2\n2:ESP3\n"))

    file = write_dataset(selector)
    writer = csv.writer(file)


    

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

                #clear the counts for next x,y
                BeaconCount['ESP_Beacon_one'] = 0
                BeaconCount['ESP_Beacon_two'] = 0
                BeaconCount['ESP_Beacon_three'] = 0

                ESP_1.clear()


                print(f"Starting sniff at ({X},{Y})")    
                sniff(iface=wlan, prn=beacon_parse, store=0, 
                      filter="type mgt subtype beacon", stop_filter = stop_sniff, timeout = 10)

                ESP1_avg = 10 * np.log10(average_RSSI(ESP_1))


                print(f"RSSI at ({X},{Y}) for {APs[selector]}: {ESP1_avg:.2f} dBm")



                writer.writerow([APs[selector], X, Y, ESP1_avg ])



            if key.name == 'esc':
                file.close()
                exit(0)

    #sniff(iface=wlan, prn=beacon_parse, store=0, filter="type mgt subtype beacon")
