import random

# Función para crear un mazo barajado
def create_shuffled_deck():
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    return deck

# Configuración del juego
deck = create_shuffled_deck()
card_count = 0

def draw_card():
    global deck, card_count
    if len(deck) == 0:  # Verifica si el mazo está vacío
        deck = create_shuffled_deck()  # Rebaraja el mazo si está vacío
        card_count = 0  # Reiniciar el conteo de cartas cuando se baraja de nuevo
    card = deck.pop()
    update_card_count(card)
    return card

def update_card_count(card):
    global card_count
    if card in ['2', '3', '4', '5', '6']:
        card_count += 1
    elif card in ['10', 'J', 'Q', 'K', 'A']:
        card_count -= 1

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
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(draw_card())
    return dealer_hand

def play_game(bet_amount):
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]
    
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

# Exponer el conteo de cartas y la función de juego
def get_card_count():
    global card_count
    return card_count
