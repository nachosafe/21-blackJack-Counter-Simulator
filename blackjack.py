import random

# Función para crear un mazo barajado de 6 barajas
def create_shuffled_deck(num_decks=6):
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4 * num_decks
    random.shuffle(deck)
    return deck

# Configuración del juego
num_decks = 6
deck = create_shuffled_deck(num_decks)
card_count = 0
running_count = 0

def draw_card():
    global deck, card_count, running_count
    if len(deck) <= num_decks * 52 * 0.4:  # Rebaraja cuando se ha usado el 60% del mazo
        deck = create_shuffled_deck(num_decks)
        card_count = 0
        running_count = 0
    card = deck.pop()
    update_card_count(card)
    return card

def update_card_count(card):
    global running_count
    hi_opt_ii_values = {
        'A': 0, '2': 1, '3': 1, '4': 2, '5': 2,
        '6': 1, '7': 1, '8': 0, '9': 0, '10': -2,
        'J': -2, 'Q': -2, 'K': -2
    }
    running_count += hi_opt_ii_values[card]

def calculate_hand_value(hand):
    value = 0
    num_aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            value += 10
        elif card == 'A':
            value += 11
            num_aces += 1
        else:
            value += int(card)
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def basic_strategy(player_hand, dealer_card):
    player_value = calculate_hand_value(player_hand)
    dealer_value = int(dealer_card) if dealer_card.isdigit() else 10 if dealer_card in ['J', 'Q', 'K'] else 11
    if player_value >= 17:
        return 'stand'
    elif player_value <= 11:
        return 'hit'
    elif player_value == 12 and 4 <= dealer_value <= 6:
        return 'stand'
    elif 13 <= player_value <= 16 and 2 <= dealer_value <= 6:
        return 'stand'
    else:
        return 'hit'

def player_turn(player_hand, dealer_card):
    while True:
        action = basic_strategy(player_hand, dealer_card)
        if action == 'hit':
            player_hand.append(draw_card())
            if calculate_hand_value(player_hand) > 21:
                break
        elif action == 'stand':
            break
    return player_hand

def dealer_turn(dealer_hand):
    while calculate_hand_value(dealer_hand) < 17 or (calculate_hand_value(dealer_hand) == 17 and 'A' in dealer_hand):
        dealer_hand.append(draw_card())
    return dealer_hand

def play_game(bet_amount):
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]
    
    # Check for blackjack (21 with first two cards)
    if calculate_hand_value(player_hand) == 21 and len(player_hand) == 2:
        if calculate_hand_value(dealer_hand) == 21 and len(dealer_hand) == 2:
            return 0  # Both player and dealer have blackjack (push)
        else:
            return bet_amount * 1.5  # Player wins with blackjack

    player_hand = player_turn(player_hand, dealer_hand[0])
    dealer_hand = dealer_turn(dealer_hand)
    
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    
    if player_value > 21:
        return -bet_amount
    elif dealer_value > 21 or player_value > dealer_value:
        return bet_amount
    elif player_value < dealer_value:
        return -bet_amount
    else:
        return 0

def get_card_count():
    global card_count
    return card_count

def get_running_count():
    global running_count
    return running_count

def get_true_count():
    num_decks = len(deck) / 52
    if num_decks == 0:
        return 0
    return running_count / num_decks
