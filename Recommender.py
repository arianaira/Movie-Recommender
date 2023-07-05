import torch
import pandas as pd
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader,random_split
from tqdm.notebook import tqdm
import numpy as np
import app

class Encoder(nn.Module):
    def __init__(self, embedd_size, embedding_size, hidden_size, num_layers=2, p=0.5):
        super(Encoder, self).__init__()
        self.dropout = nn.Dropout(p)
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lin = nn.Linear(1, embedding_size)

        self.embedding = nn.Embedding(embedd_size, embedding_size)
        self.rnn = nn.GRU(2*embedding_size, hidden_size, num_layers, dropout=p)
        self.relu = nn.ReLU()

    def forward(self, x):
        # x shape: (seq_length, N, 2) where N is batch size

        rate = self.dropout(self.relu(self.lin(x[:,:,1].unsqueeze(-1).to(torch.float32))))
        embedding = self.dropout(self.embedding(x[:,:,0]))
        # embedding shape: (seq_length, N, embedding_size)

        _, hidden = self.rnn(torch.cat([rate, embedding], dim=-1))
        # outputs shape: (seq_length, N, hidden_size)

        return hidden


class Decoder(nn.Module):
    def __init__(
        self, embedd_size, embedding_size, hidden_size, output_size, num_layers=2, p=0.5
    ):
        super(Decoder, self).__init__()
        self.dropout = nn.Dropout(p)
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(embedd_size, embedding_size)
        self.lin = nn.Linear(embedding_size, embedding_size)
        self.rnn = nn.GRU(embedding_size, hidden_size, num_layers, dropout=p)
        self.fc = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x, hidden):
        # x shape: (N) where N is for batch size, we want it to be (1, N), seq_length
        x = x.unsqueeze(0).to(torch.int)
        
    
        embedding = self.dropout(self.embedding(x))
        
        # embedding shape: (1, N, embedding_size)
        embedding = self.relu(self.dropout(self.lin(embedding)))

        outputs, hidden = self.rnn(embedding, hidden)
        # outputs shape: (1, N, hidden_size)

        predictions = self.relu(self.fc(outputs))

        # predictions shape: (1, N, 1) to send it to
        # just gonna remove the first dim
        predictions = predictions.squeeze(0).squeeze(-1)

        return predictions, hidden


class RecSys(nn.Module):
    def __init__(self, num_items, embedding_size, hidden_size, num_layers, device, p=0.5):
        super(RecSys, self).__init__()

        self.encoder = Encoder(num_items, embedding_size, hidden_size, num_layers, p)
        self.decoder = Decoder(num_items, embedding_size, hidden_size, 1, num_layers, p)
        self.device = device
        self.to(device)

    def forward(self, source, decode_token): # source : <B, S, 2> , decode_token: <B>
        hidden = self.encoder(source.permute((1,0,2)))

        # Grab the first input to the Decoder which will be <SOS> token
        x = decode_token
        
        # Use previous hidden, cell as context from encoder at start
        output, _ = self.decoder(x, hidden)

        return output
    
    def pred(self, source, decode_token):
        self.eval()
        with torch.no_grad():
            return self.forward(source, decode_token)


def get_top_rated_movies(user_hist, model, movie_ids, device, num_recommendation=10): # user_hist : <Sequence , 2>
    ratings = []
    
    # Pass user ID and each movie ID through the model
    for movie_id in movie_ids:
        source , decode_token = torch.tensor(user_hist, dtype=torch.int64).unsqueeze(0).to(device) , torch.tensor([movie_id]).to(device).to(torch.int64)

        rating = model.pred(source, decode_token)  # source : <1, S, 2> , decode_token: <1>
        
        ratings.append((movie_id, rating.item()))
    
    # Sort the ratings in descending order
    sorted_ratings = sorted(ratings, key=lambda x: x[1], reverse=True)
    
    # Get the top 10 rated movies' IDs
    top_movies = [movie_id for movie_id, _ in sorted_ratings[:num_recommendation]]
    
    return top_movies




