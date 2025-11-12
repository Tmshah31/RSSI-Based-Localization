from scapy.all import * 
APs = ["ESP_Beacon_one", "ESP_Beacon_two", "ESP_Beacon_three"]
flags = [0,0,0] #[RSSI_AP1 -> RSSI_AP3]

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
            exit(0)

if __name__ == "__main__":

    sniff(iface="wlx00c0cab9a65f", prn=beacon_parse, store=0, filter="type mgt subtype beacon")
