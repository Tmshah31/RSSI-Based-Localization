from scapy.all import * 
import os
import time
import keyboard


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
    values = []
    return avg

def beacon_parse(packet):
    if(packet.haslayer(Dot11Beacon) and packet.haslayer(RadioTap)):
        ssid = packet[Dot11Elt].info.decode('utf-8')
        if(ssid == APs[0] and BeaconCount['ESP_Beacon_one'] < 5):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            sig_linear = 10^(sig_strength/10)
            ESP_1.append(sig_linear)
            BeaconCount['ESP_Beacon_one'] += 1 
        elif(ssid == APs[1] and BeaconCount['ESP_Beacon_two'] < 5):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            sig_linear = 10^(sig_strength/10)
            ESP_2.append(sig_linear)
            BeaconCount['ESP_Beacon_two'] += 1
        elif(ssid == APs[2] and BeaconCount['ESP_Beacon_three'] < 5):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            sig_linear = 10^(sig_strength/10)
            ESP_3.append(sig_linear)
            BeaconCount['ESP_Beacon_three'] += 1

        if(BeaconCount["ESP_Beacon_one"] == 5 and BeaconCount["ESP_Beacon_two"] == 5 and BeaconCount['ESP_Beacon_three'] == 5):
            print("Found all SSID beacons")

            #clear the counts for next x,y
            BeaconCount['ESP_Beacon_one'] = 0
            BeaconCount['ESP_Beacon_two'] = 0
            BeaconCount['ESP_Beacon_three'] = 0

            return

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
            if key.name == 'esc':
                exit(0)

    #sniff(iface=wlan, prn=beacon_parse, store=0, filter="type mgt subtype beacon")
