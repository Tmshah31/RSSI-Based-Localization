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

#global variables so they can be access from data write function
X = 0
Y = 0

#store the signal strength values -> make sure to convert into linear before adding them into the list 
#These arrays need to be cleared before the beacon_parse returns to get them ready for the next run 
ESP_1 = []
ESP_2 = []
ESP_3 = []


def average_RSSI(values):
    total = sum(values)
    avg = total/len(values)
    return avg


def stop_sniff(packet):

    return (BeaconCount["ESP_Beacon_one"] == 5 and BeaconCount["ESP_Beacon_two"] == 5 and BeaconCount['ESP_Beacon_three'] == 5)

def beacon_parse(packet):
    if(packet.haslayer(Dot11Beacon) and packet.haslayer(RadioTap)):
        ssid = packet[Dot11Elt].info.decode('utf-8')
        if(ssid == APs[0] and BeaconCount['ESP_Beacon_one'] < 5):
            sig_strength = packet[RadioTap].dBm_AntSignal
            #print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            sig_linear = 10**(sig_strength/10)
            ESP_1.append(sig_linear)
            BeaconCount['ESP_Beacon_one'] += 1 
        elif(ssid == APs[1] and BeaconCount['ESP_Beacon_two'] < 5):
            sig_strength = packet[RadioTap].dBm_AntSignal
            #print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            sig_linear = 10**(sig_strength/10)
            ESP_2.append(sig_linear)
            BeaconCount['ESP_Beacon_two'] += 1
        elif(ssid == APs[2] and BeaconCount['ESP_Beacon_three'] < 5):
            sig_strength = packet[RadioTap].dBm_AntSignal
            #print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            sig_linear = 10**(sig_strength/10)
            ESP_3.append(sig_linear)
            BeaconCount['ESP_Beacon_three'] += 1

        if(BeaconCount["ESP_Beacon_one"] == 5 and BeaconCount["ESP_Beacon_two"] == 5 and BeaconCount['ESP_Beacon_three'] == 5):
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


def write_dataset(AP):

    csv_header = ['SSID', "X", "Y", "RSSI (avg)"]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_name = Path("/home/tmshah") / "RSSI_Localization" / "RSSI-Based-Localization" / "data" / f"{APs[AP]}_{timestamp}_dataset.csv"

    csvfile = open(csv_name, 'w', newline='')

    csv_writer = csv.writer(csvfile)

    csv_writer.writerow(csv_header)



    return csvfile, csv_writer


    
if __name__ == "__main__":

    #Monitor_mode()

    files = []
    writer = []

    for i in range (3):
        f,w = write_dataset(i) 
        files.append(f)
        writer.append(w)

    

    

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
                ESP_2.clear()
                ESP_3.clear()


                print(f"Starting sniff at ({X},{Y})")    
                sniff(iface=wlan, prn=beacon_parse, store=0, filter="type mgt subtype beacon", stop_filter = stop_sniff)

                ESP1_avg = 10 * np.log10(average_RSSI(ESP_1))
                ESP2_avg = 10 * np.log10(average_RSSI(ESP_2))
                ESP3_avg = 10 * np.log10(average_RSSI(ESP_3))


                print(f'RSSI values at: ({X},{Y})')
                print("ESP1 RSSI average: ", ESP1_avg)
                print("ESP2 RSSI average: ", ESP2_avg)
                print("ESP3 RSSI average: ", ESP3_avg)

                writer[0].writerow([APs[0], X, Y, ESP1_avg ])
                writer[1].writerow([APs[1], X, Y, ESP2_avg ])
                writer[2].writerow([APs[2], X, Y, ESP3_avg ])


            if key.name == 'esc':
                for i in range(3):
                    files[i].close()
                exit(0)
