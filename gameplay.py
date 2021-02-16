#%%
import random
from functools import partial

class Player:
    def __init__(self, number, cards):
        self.number = number
        self.cards = cards
    
    def __repr__(self):
        return f"Player {self.number}, Cards {self.cards}"

class Game:
    def __init__(self):
        self.non_measure_cards = ["SWAP", "Toffoli", "Hadamard", "CNOT", "CNOT", "CNOT", "X", "X", "X"]
        random.shuffle(self.non_measure_cards)
        self.players = [Player(1, self.non_measure_cards[0:3]), Player(2, self.non_measure_cards[3:6]), Player(3, self.non_measure_cards[6:])]
        for player in self.players:
            player.cards.append("Measure")
#%%
g = Game()
print(g.players)
#%%
def yo(string1, string2):
    print(f"{string1} {string2}")

#%%