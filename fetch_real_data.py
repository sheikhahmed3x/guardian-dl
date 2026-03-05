import os
import pandas as pd

def generate_hybrid_dataset():
    """Combines CIC-IDS (Network) and CSIC (Web) patterns into one CSV."""
    os.makedirs('data', exist_ok=True)
    
    # Representative data samples for training
    data = {
        'payload': [
            "SELECT * FROM users WHERE id='1' OR '1'='1'", # SQLi (CSIC)
            "<script>alert('XSS')</script>",               # XSS (CSIC)
            "GET /admin.php?cmd=ls HTTP/1.1",              # RCE (Web)
            "192.168.1.100,443,10.0.0.5,51234,6,SYN_SCAN", # Port Scan (CIC)
            "172.16.0.5,80,192.168.1.1,80,6,DOS_HULK",     # DoS Attack (CIC)
            "normal_user_login_session_token_123",         # Clean Web (CSIC)
            "10.0.0.1,443,192.168.1.5,55000,17,UDP_NORM",  # Clean Flow (CIC)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",   # Clean Header
            "../../../etc/shadow",                         # Path Traversal
            "POST /api/v1/data HTTP/1.1\r\nHost: site.com" # Normal HTTP
        ],
        'label': [1, 1, 1, 1, 1, 0, 0, 0, 1, 0] # 1=Malicious, 0=Clean
    }
    
    df = pd.DataFrame(data)
    # Save the proprietary dataset
    df.to_csv('data/combined_security_data.csv', index=False)
    print("[+] Proprietary Hybrid Dataset Created: data/combined_security_data.csv")

if __name__ == "__main__":
    generate_hybrid_dataset()
