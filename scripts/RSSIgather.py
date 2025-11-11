from scapy.all import * 

def beacon_parse(packet):
    if(packet.haslayer(Dot11Beacon) and packet.haslayer(Radiotap)):
        ssid = packet[Dot11Elt].info.decode('utf-8')
        if(ssid == "ESP_Beacon_One"):
            sig_strength = packet[Radiotap].dBm_Antsignal
            print(f"SSID: {ssid}\nSignal Strength: {sig_strength}")


if __name__ == "__main__":
    sniff(iface = "wlx00c0cab9a65f", prn = beacon_parse)