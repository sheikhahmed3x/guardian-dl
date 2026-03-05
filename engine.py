import torch
import torch.nn as nn
import torch.nn.functional as F

class GuardianDL(nn.Module):
    def __init__(self, vocab_size=256, embed_dim=64, hidden_dim=128):
        super(GuardianDL, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        
        # CNN: Captures local patterns (e.g., 'SELECT', '<script>')
        self.conv = nn.Conv1d(embed_dim, 128, kernel_size=3, padding=1)
        
        # LSTM: Captures the order of commands (The 'story' of the attack)
        self.lstm = nn.LSTM(128, hidden_dim, batch_first=True, bidirectional=True)
        
        # Dense classification layers
        self.fc = nn.Linear(hidden_dim * 2, 1)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        # x: [Batch, Seq_Len]
        x = self.embedding(x).transpose(1, 2) # [Batch, Embed, Seq]
        x = F.relu(self.conv(x)).transpose(1, 2) # [Batch, Seq, 128]
        
        _, (hn, _) = self.lstm(x) # Bi-LSTM hidden state
        x = torch.cat((hn[0], hn[1]), dim=1) # Concatenate forward/backward
        
        x = self.dropout(x)
        return torch.sigmoid(self.fc(x))

def string_to_tensor(text, max_len=200):
    """Encodes text into ASCII tensors."""
    encoded = [ord(c) if ord(c) < 256 else 0 for c in text]
    if len(encoded) > max_len:
        encoded = encoded[:max_len]
    else:
        encoded += [0] * (max_len - len(encoded))
    return torch.tensor([encoded], dtype=torch.long)

def get_threat_score(text):
    """Runs a forward pass on the proprietary model."""
    model = GuardianDL()
    # model.load_state_dict(torch.load("weights.pth")) # Point to your weights here
    model.eval()
    
    with torch.no_grad():
        input_tensor = string_to_tensor(text)
        return model(input_tensor).item()
