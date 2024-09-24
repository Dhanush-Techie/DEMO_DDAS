# from scapy.all import sniff, IP, TCP
# import time

# # Callback function to process each captured packet
# def packet_callback(packet):
#     if packet.haslayer(TCP):
#         # Check if the packet is HTTP (port 80) or HTTPS (port 443)
#         if packet[TCP].dport == 80 or packet[TCP].dport == 443:
#             if packet.haslayer(IP):
#                 src_ip = packet[IP].src
#                 dst_ip = packet[IP].dst
#                 tcp_len = len(packet[TCP].payload)

#                 # Log detected downloads to a file
#                 with open("download_log.txt", "a") as log_file:
#                     log_entry = f"{time.ctime()} - Possible file download detected from {src_ip} to {dst_ip} over port {packet[TCP].dport}. Data length: {tcp_len} bytes\n"
#                     log_file.write(log_entry)

#                 # Print to console as well
#                 print(f"Detected: {log_entry}")

# # Sniff traffic on the network interface
# def start_sniffing(interface):
#     print(f"Monitoring network interface: {interface} for file downloads...")
#     sniff(iface=interface, filter="tcp port 80 or tcp port 443", prn=packet_callback, store=False)

# if __name__ == "__main__":
#     # Replace 'eth0' with the actual network interface you're monitoring
#     interface = "Wi-Fi"  # Linux Example: eth0, Windows Example: use "Wi-Fi" or "Ethernet"
#     start_sniffing(interface)


from scapy.all import sniff, IP, TCP

# Callback function to process each captured packet
def packet_callback(packet):
    if packet.haslayer(TCP):
        # Check if the packet is HTTP (port 80) or HTTPS (port 443)
        if packet[TCP].dport == 80 or packet[TCP].dport == 443:
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                tcp_len = len(packet[TCP].payload)
                
                # Check for significant data size, which could indicate a file download
                if tcp_len > 1000:  # Adjust this threshold as needed
                    print(f"Potential file download detected from {src_ip} to {dst_ip} over port {packet[TCP].dport}")
                    print(f"Data length: {tcp_len} bytes")
                    print(packet.summary())

# Sniff traffic on the network interface
def start_sniffing(interface):
    print(f"Monitoring network interface: {interface} for file downloads...")
    # Start sniffing on the given network interface, filtering for HTTP and HTTPS traffic
    sniff(iface=interface, filter="tcp port 80 or tcp port 443", prn=packet_callback, store=False)

if __name__ == "__main__":
    # Replace 'eth0' with the actual network interface you're monitoring
    interface = "Wi-Fi"  # Linux Example: eth0, Windows Example: use "Wi-Fi" or "Ethernet"
    start_sniffing(interface)
