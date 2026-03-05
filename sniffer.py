from scapy.all import sniff, IP, TCP, Raw
from engine import get_threat_score
import time

def process_packet(packet):
    # Only look at packets with a data payload (Layer 7)
    if packet.haslayer(Raw):
        try:
            # Decode the raw bytes into a string
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            
            if len(payload.strip()) > 5:
                # Get the score from your CNN-LSTM model
                score = get_threat_score(payload)
                
                # Logic for real-time alerting
                if score > 0.85:
                    print(f"\n[!] ALERT: CRITICAL THREAT DETECTED")
                    print(f"    Source: {packet[IP].src} -> Dest: {packet[IP].dst}")
                    print(f"    Payload Preview: {payload[:50]}...")
                    print(f"    AI Confidence: {score:.4f}")
                elif score > 0.50:
                    print(f"[*] Suspicious Activity from {packet[IP].src} (Score: {score:.4f})")
        except Exception:
            pass

if __name__ == "__main__":
    print("[*] Guardian-DL Live Sniffer Active. Monitoring interface: eth0/wlan0...")
    # Change 'iface' to your actual interface (e.g., 'wlan0' or 'eth0')
    sniff(prn=process_packet, store=0)
