from scapy.all import sniff, IP, TCP, Raw
import hashlib
import re

# Set of downloadable content types
downloadable_content_types = {
    'application/pdf',
    'application/zip',
    'application/octet-stream',  # General binary data
    'video/mp4',
    'image/jpeg',
    'image/png',
}

# Dictionary to hold incremental hash states by flow (source IP, destination IP, destination port)
hash_state = {}

# Function to update hash with the packet's data
def update_hash(flow_id, payload):
    if flow_id not in hash_state:
        hash_state[flow_id] = hashlib.blake2b()
    
    hash_state[flow_id].update(payload)

# Callback function to process each captured packet
def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        if packet[TCP].dport == 80 or packet[TCP].dport == 443:
            # Check for HTTP responses
            if packet.haslayer(Raw):
                payload = packet[Raw].load.decode(errors='ignore')  # Decode the payload

                # Check if it's an HTTP response (look for Content-Type header)
                if 'HTTP/' in payload:
                    headers, _ = payload.split('\r\n\r\n', 1)
                    for line in headers.split('\r\n'):
                        if line.startswith('Content-Type:'):
                            content_type = line.split(': ')[1]
                            if content_type in downloadable_content_types:
                                flow_id = (packet[IP].src, packet[IP].dst, packet[TCP].dport)
                                update_hash(flow_id, payload.encode())
                                print(f"Captured download of type '{content_type}' from {packet[IP].src} to {packet[IP].dst}")

                # Check for the end of the TCP connection
                if packet[TCP].flags == 'FA':
                    flow_id = (packet[IP].src, packet[IP].dst, packet[TCP].dport)
                    if flow_id in hash_state:
                        final_hash = hash_state[flow_id].hexdigest()
                        print(f"Download complete for flow {flow_id}. Final hash: {final_hash}")
                        del hash_state[flow_id]

def start_sniffing(interface):
    print(f"Monitoring network interface: {interface} for file downloads...")
    sniff(iface=interface, filter="tcp port 80 or tcp port 443", prn=packet_callback, store=False)

if __name__ == "__main__":
    interface = "Wi-Fi"  # Replace with your actual network interface
    start_sniffing(interface)
