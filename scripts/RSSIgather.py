from scapy.all import * 
APs = ["ESP_Beacon_one", "ESP_Beacon_two", "ESP_Beacon_three"]

def beacon_parse(packet):
    if(packet.haslayer(Dot11Beacon) and packet.haslayer(RadioTap)):
        ssid = packet[Dot11Elt].info.decode('utf-8')
        if(ssid == APs[0]):
            sig_strength = packet[RadioTap].dBm_AntSignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")
            exit(0)


if __name__ == "__main__":

    sniff(iface="wlx00c0cab9a65f", prn=beacon_parse, store=0, filter="type mgt subtype beacon")
