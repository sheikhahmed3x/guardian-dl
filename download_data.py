import pandas as pd
import os

def create_mock_training_data():
    """Generates a small training set to test the pipeline before full download."""
    data = {
        'payload': [
            "SELECT * FROM users WHERE id='1' OR '1'='1'",
            "<script>alert('xss')</script>",
            "GET /index.html HTTP/1.1",
            "../../../etc/passwd",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        ],
        'label': [1, 1, 0, 1, 0] # 1 = Malicious, 0 = Clean
    }
    df = pd.DataFrame(data)
    df.to_csv('data/combined_security_data.csv', index=False)
    print("[+] Mock dataset created for pipeline testing.")

if __name__ == "__main__":
    if not os.path.exists('data'): os.makedirs('data')
    create_mock_training_data()
