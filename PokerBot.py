import random
import time
import math


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0


def create_deck():
    deck = []
    symbols = ['S', 'H', 'C', 'D'] # spade, heart, clubs, diamond

    for rank in range(2, 15):
        for symbol in symbols:
            card = (rank, symbol)
            deck.append(card)

    return deck


def draw_card(deck):
    random_card = random.randrange(len(deck))
    card = deck.pop(random_card)
    return card


def get_hand_strength(hand, community_cards):
    


def ucb1(node):
    if node.visits == 0:
        return float('inf')
    return node.wins / node.visits + math.sqrt(2 * math.log(node.parent.visits) / node.visits)


def mcts(deck):
    start_time = time.time()
    while time.time() - start_time < 10:
        # Simulate a game from the current state
        # Update the tree with the result of the simulation
        pass
    

if __name__ == "__main__":
    deck = create_deck()
    bot_cards = []
    opp_cards = []
    community_cards = []

    mcts(deck)

    # Pre-Flop
    bot_cards.append(draw_card(deck))
    bot_cards.append(draw_card(deck))
    opp_cards.append(draw_card(deck))
    opp_cards.append(draw_card(deck))

