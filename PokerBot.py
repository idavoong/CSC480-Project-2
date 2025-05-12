import random
import time
import math
from collections import defaultdict
from itertools import combinations


class Node:
    def __init__(self, bot_cards, com_cards, opp_cards, parent=None):
        self.bot_cards = bot_cards
        self.com_cards = com_cards
        self.opp_cards = opp_cards
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.ucb1 = float('inf')

    def update_ucb1(self, c=math.sqrt(2)):
        if self.visits == 0:
            self.ucb1 = float('inf')
        else:
            self.ucb1 = (self.wins / self.visits) + (c * math.sqrt(math.log(self.parent.visits) / self.visits))


def create_deck():
    deck = []
    symbols = ['S', 'H', 'C', 'D'] # spade, heart, clubs, diamond

    for rank in range(2, 15): # 2-10, J(11), Q(12), K(13), A(14)
        for symbol in symbols:
            card = (rank, symbol)
            deck.append(card)

    return deck


def draw_card(deck):
    random_card = random.randrange(len(deck))
    card = deck.pop(random_card)
    return card


def has_straight(ranks):
    ranks = sorted(set(ranks))
    if 14 in ranks: # Ace(1) can be used as low in a straight
        ranks = [1] + ranks 

    highest = None # return highest straight
    for i in range(len(ranks) - 4):
        window = ranks[i:i+5]
        if window[-1] - window[0] == 4: 
            highest = window[-1]

    if highest:
        return True, highest
    return False, None


def get_hand_rank(hand, community_cards):
    '''
    9 - Royal Flush
    8 - Straight Flush
    7 - Four of a Kind
    6 - Full House
    5 - Flush
    4 - Straight
    3 - Three of a Kind
    2 - Two Pair
    1 - One Pair
    0 - High Card
    '''

    all_cards = hand + community_cards
    num_count = defaultdict(int)
    suit_count = defaultdict(list)

    for rank, suit in all_cards:
        num_count[rank] += 1
        suit_count[suit].append(rank)

    unique_ranks = sorted(set([rank for rank, _ in all_cards]), reverse=True)

    # Check for Flush
    flush_suit = None
    flush_ranks = []
    for suit, ranks in suit_count.items():
        if len(ranks) >= 5:
            flush_suit = suit
            flush_ranks = sorted(ranks, reverse=True)
            break

    # Check for Straight
    all_ranks = [rank for rank, _ in all_cards]
    has_str, high_card = has_straight(all_ranks)

    # Straight Flush / Royal Flush
    has_sf, high_sf = False, None
    if flush_suit:
        flush_only_ranks = [rank for rank in suit_count[flush_suit]]
        has_sf, high_sf = has_straight(flush_only_ranks)
        if has_sf and high_sf == 14:  # Ace-high straight flush = Royal Flush
            return (9, [14])

    counts = sorted(num_count.values(), reverse=True)

    if has_sf: # Straight Flush
        return (8, [high_sf]) 
    elif 4 in counts: # Four of a Kind
        return (7, [k for k, v in num_count.items() if v == 4])
    elif 3 in counts and 2 in counts: # Full House
        return (6, [k for k, v in num_count.items() if v == 3])
    elif flush_suit: # Flush
        return (5, flush_ranks[:5])
    elif has_str: # Straight
        return (4, [high_card])
    elif 3 in counts: # Three of a Kind
        return (3, [k for k, v in num_count.items() if v == 3])
    elif counts.count(2) >= 2: # Two Pair
        return (2, sorted([k for k, v in num_count.items() if v == 2], reverse=True)[:2])
    elif 2 in counts: # One Pair
        return (1, [k for k, v in num_count.items() if v == 2])
    else: # High Card
        return (0, unique_ranks[:5])


def ucb1(node, c = math.sqrt(2)): # c = sqrt(2)
    if node.visits == 0:
        return float('inf')
    return (node.wins / node.visits) + (c * math.sqrt(math.log(node.parent.visits) / node.visits))


def mcts(deck, bot_cards, com_cards):
    root = Node(bot_cards, com_cards, [])
    start_time = time.time()

    while time.time() - start_time < 10:        
        # draw opp cards
        opp_cards = [draw_card(deck), draw_card(deck)]
        child_node = Node(bot_cards, com_cards, opp_cards, parent=root)
        root.children.append(child_node)

        # draw remaining community cards
        temp_com_cards = []
        for _ in range(5 - len(com_cards)):
            temp_com_cards.append(draw_card(deck))

        # evaluate hand
        bot_rank = get_hand_rank(bot_cards, com_cards + temp_com_cards)
        opp_rank = get_hand_rank(opp_cards, com_cards + temp_com_cards)

        # update wins, visits, and ucb1
        if bot_rank[0] > opp_rank[0]:
            child_node.wins += 1
            root.wins += 1
        child_node.visits += 1
        root.visits += 1
        child_node.update_ucb1()

        # add cards back to deck
        deck.append(opp_cards[0])
        deck.append(opp_cards[1])
        for card in temp_com_cards:
            deck.append(card)
    
    print("root visits:", root.visits)
    print("root wins:", root.wins)
    return root.wins / root.visits
    

if __name__ == "__main__":
    deck = create_deck()
    bot_cards = []
    opp_cards = []
    community_cards = []

    # Pre-Flop
    bot_cards.append(draw_card(deck))
    bot_cards.append(draw_card(deck))
    opp_cards.append(draw_card(deck))
    opp_cards.append(draw_card(deck))

    result = mcts(deck, bot_cards, community_cards)
    print("Win rate:", result)
    print("Bot cards:", bot_cards)
    print("Community cards:", community_cards)
    print("Opponent cards:", opp_cards)
    print()

    # Flop
    community_cards.append(draw_card(deck))
    community_cards.append(draw_card(deck))
    community_cards.append(draw_card(deck))

    result = mcts(deck, bot_cards, community_cards)
    print("Win rate:", result)
    print("Bot cards:", bot_cards)
    print("Community cards:", community_cards)
    print("Opponent cards:", opp_cards)
    print()

    # Turn
    community_cards.append(draw_card(deck))

    result = mcts(deck, bot_cards, community_cards)
    print("Win rate:", result)
    print("Bot cards:", bot_cards)
    print("Community cards:", community_cards)
    print("Opponent cards:", opp_cards)
    print()

    # River
    community_cards.append(draw_card(deck))
    bot_hand = get_hand_rank(bot_cards, community_cards)
    opp_hand = get_hand_rank(opp_cards, community_cards)
    print("Community cards:", community_cards)
    print("Bot hand:", bot_hand)
    print("Opponent hand:", opp_hand)

    # bot_cards = [(7, 'C'), (7, 'D')]
    # opp_cards = [(13, 'D'), (7, 'H')]
    # community_cards = [(8, 'D'), (8, 'H'), (11, 'C'), (12, 'S')]

    # print(get_hand_rank(bot_cards, community_cards))
    # print(get_hand_rank(opp_cards, community_cards))
