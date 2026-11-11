import random
import statistics
# Please feel free to work with your own code structure

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}

# 2 example poker hands
example_hand1 = ['Ad', '2s', '2c']
example_hand2 = ['5s', '5c', '5d']

# All 52 cards in the deck.
ranks = "23456789TJQKA"
suits = "shdc"
deck = []
for rank in ranks:
    for suit in suits:
        deck.append(rank + suit)
    



# Randomly generate two hands of n cards
def generate_2hands(nn_card=3):
    """
    Return two hands of cards, each hand consists of nn_card number of cards.
    Note that there shall be no duplicates.

    Parameters
    ----------
    nn_card : int
            Number of cards in each hand

    Returns
    -------
    out : lists of strings
        Two lists, each corresponding to one hand
    """
    picked = random.sample(deck, nn_card * 2)
    hand1 = picked[0:nn_card]
    hand2 = picked[nn_card:nn_card * 2]
    return hand1, hand2


#value of a card's rank: 2->1, 3->2 ....
def rank_value(card):
    rank = card[0]
    value = ranks.index(rank) + 1
    return value

#list with only the ranks of the card
def get_ranks(hand):
    ranks = []
    for card in hand:
        ranks.append(card[0])
    return ranks

#List with the value of the each card
def get_values(hand):
    values = []
    for card in hand:
        values.append(rank_value(card))
    return values


# identify hand category using IF-THEN rule
def identify_hand(hand_):
    """
    Identify the type and the strength of one hand.

    Notes
    ----------
    We only work with hands with three cards in this exercise, hence, there are three types available, i.e. high cards, one pair,       three of a kind.


    Parameters
    ----------
    Hand_ : list of strings
          Player hands, a list of three strings

    Returns
    -------
    out : string, int
        This function should return the type, and the strength of the given hand.
    """
    hand_ranks = get_ranks(hand_)
    for rank in hand_ranks:
        if hand_ranks.count(rank) == 3:
            return "three of a kind", rank_value(rank)
        elif hand_ranks.count(rank) == 2:
            return "pair", rank_value(rank)
    return "high card", max(get_values(hand_))


    #for c1 in hand_:
    #    for c2 in hand_:
    #        if (c1[0] == c2[0]) and (c1[1] < c2[1]):
    #            yield dict(name='pair',rank=c1[0],suit1=c1[1],suit2=c2[1])

# Print out the result
def analyse_hand(hand_):
    """
    Evaluates a given hand based on its type and strength, and return an integer value.

    Notes
    ----------
    This function should call identify_hand(...) and evaluate it based on its type and the strength.
    high cards: 1 - 13
    pairs: 14 - 26
    three-of-a-kind: 27 - 39


    Parameters
    ----------
    Hand_ : list of strings
          Player hands, a list of three strings

    Returns
    -------
    out : int
        A value refecting the overall strength of a hand.
    """
    hand_type, value = identify_hand(hand_)
    if hand_type == "three of a kind":
        score = 26 + value
    elif hand_type == "pair":
        score = 13 + value
    else:
        score = value
    return score


# Agent 2a: random agent - bids random amount, ignores all input.

def random_agent(hand, round_number, opponent_bids):
    bid = random.randint(0, 50)
    return bid


# Agent 2b: fixed agent - follows a pre-specified bid sequence, ignores all input
def fixed_agent(hand, round_number, opponent_bids):
    bids = [10, 25, 40]
    bid = bids[round_number - 1]
    return bid


# Agent 2e: reflex agent - bids based on the strength of its own hand.
def reflex_agent(hand, round_number, opponent_bids):
    score = analyse_hand(hand)
    if score >= 27:
        bid = 45
    elif score >= 14:
        bid = 25
    else:
        bid = 10
    return bid


#########################
#      Game flow        #
#########################

# play one hand between two agents.
# Returns how much money agent1 and agent2 won in this hand.
def play_hand(agent1, agent2):
    # Phase 1: card dealing
    hand1, hand2 = generate_2hands()

    # Phase 2: bidding (3 round)
    pot = 0
    bids1 = []
    bids2 = []
    for round_number in range(1, 4):
        bid1 = agent1(hand1, round_number, bids2)
        bid2 = agent2(hand2, round_number, bids1)
        pot += bid1 + bid2
        bids1.append(bid1)
        bids2.append(bid2)

    # phase 3: showdown - both hands are revealed
    score1 = analyse_hand(hand1)
    score2 = analyse_hand(hand2)
    if score1 > score2:
        return pot, 0
    elif score2 > score1:
        return 0, pot
    else:
        return pot / 2, pot / 2





# Play one game (50 hands) between two agents.
# Returns the difference in winnings: agent1's total minus agent2's total.
def play_game(agent1, agent2, n_hands=50):
    total1 = 0
    total2 = 0
    for hand_number in range(n_hands):
        won1, won2 = play_hand(agent1, agent2)
        total1 += won1
        total2 += won2
    return total1 - total2



# Play many games (100 by default) and collect the result of each game.
# Return a list with the winning difference of every game.
def run_experiment(agent1, agent2, n_games=100):
    results = []
    for game_number in range(n_games):
        diff = play_game(agent1, agent2)
        results.append(diff)
    return results



def print_results(name1, name2, results):
    mean = statistics.mean(results)
    std = statistics.stdev(results)
    print(name1, "vs", name2)
    print("  mean:", round(mean, 1), "  std:", round(std, 1))
    if mean > 0:
        print("  ->", name1, "won more money on average")
    else:
        print("  ->", name2, "won more money on average")
    print()


# writing your test code here


# Step-by-step test of one hand: reflex agent (agent 1) vs random agent (agent 2)
# Phase 1: card dealing
hand1, hand2 = generate_2hands()
print("Agent 1 got", hand1, "| Agent 2 got", hand2)

# Phase 2: bidding, 3 rounds
pot = 0
for round_number in range(1, 4):
    bid1 = reflex_agent(hand1, round_number, [])
    bid2 = random_agent(hand2, round_number, [])
    pot += bid1 + bid2
    print("Round", round_number, ": Agent 1 bids", bid1, "| Agent 2 bids", bid2, "| pot", pot)

# Phase 3: showdown
score1 = analyse_hand(hand1)
score2 = analyse_hand(hand2)
print("Showdown: Agent 1 score", score1, "| Agent 2 score", score2, "| pot", pot)



# Print the result of a match: mean and standard deviation of the

# 2d: random agent vs fixed agent, 100 games x 50 hands
print_results("Random", "Fixed", run_experiment(random_agent, fixed_agent))

# 2e: reflex agent first against random agent, then against fixed agent
print_results("Reflex", "Random", run_experiment(reflex_agent, random_agent))
print_results("Reflex", "Fixed", run_experiment(reflex_agent, fixed_agent))