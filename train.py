import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from engine import GuardianDL, string_to_tensor

def train_model():
    # 1. Load Dataset
    df = pd.read_csv('data/combined_security_data.csv')
    
    # 2. Initialize Model, Loss, and Optimizer
    model = GuardianDL()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print("[*] Starting Training on Combined CIC/CSIC Data...")
    
    # 3. Training Loop (Simplified for demo)
    model.train()
    for epoch in range(10):
        total_loss = 0
        for _, row in df.iterrows():
            optimizer.zero_grad()
            
            # Convert string to tensor
            input_tensor = string_to_tensor(row['payload'])
            label = torch.tensor([[float(row['label'])]], dtype=torch.float32)
            
            # Forward pass
            output = model(input_tensor)
            loss = criterion(output, label)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        print(f"Epoch {epoch+1}/10 | Loss: {total_loss/len(df):.4f}")

    # 4. Save the Intellectual Property
    torch.save(model.state_dict(), "guardian_v1.pth")
    print("[+] Training Complete. Weights saved to guardian_v1.pth")

if __name__ == "__main__":
    train_model()
