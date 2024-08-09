import random

# Definir las cartas y los valores
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck = [f'{value} of {suit}' for value in values.keys() for suit in suits]

# Crear 6 barajas y mezclarlas antes de cada partida
def shuffle_deck():
    deck = [f'{value} of {suit}' for value in values.keys() for suit in suits] * 6
    random.shuffle(deck)
    return deck

# Función para repartir una carta
def deal_card(deck):
    return deck.pop()

# Función para calcular el valor de la mano
def calculate_hand_value(hand):
    value = sum(values[card.split()[0]] for card in hand)
    num_aces = sum(1 for card in hand if 'A' in card)
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

# Función para mostrar la mano
def show_hand(hand, hidden=False):
    if hidden:
        return f"{hand[0]} y [carta oculta]"
    else:
        return ", ".join(hand)

# Función para realizar una apuesta
def place_bet(balance):
    while True:
        try:
            bet = int(input(f"Tienes ${balance}. ¿Cuánto quieres apostar? "))
            if 1 <= bet <= balance:
                return bet
            else:
                print(f"Apuesta inválida. Debes apostar entre $1 y ${balance}.")
        except ValueError:
            print("Por favor, ingresa una cantidad válida.")

# Función para manejar la apuesta segura
def insurance_bet(balance, bet):
    while True:
        try:
            insurance = input("¿Quieres hacer una apuesta segura? (sí/no): ").lower()
            if insurance == 'sí':
                if balance >= bet / 2:
                    print(f"Apuesta segura de ${bet / 2} realizada.")
                    return bet / 2
                else:
                    print("No tienes suficiente saldo para hacer una apuesta segura.")
                    return 0
            elif insurance == 'no':
                return 0
            else:
                print("Respuesta inválida. Responde 'sí' o 'no'.")
        except ValueError:
            print("Por favor, ingresa una cantidad válida.")

# Función para manejar la división de la mano
def split_hand(deck, hand, balance, bet):
    split_hands = [[hand[0]], [hand[1]]]
    new_bet = bet

    for i in range(2):
        split_hands[i].append(deal_card(deck))
        print(f"Mano dividida {i + 1}: {show_hand(split_hands[i])}")

    # Jugar cada mano dividida
    for i, hand in enumerate(split_hands):
        while True:
            action = input(f"Para la mano {i + 1}: ¿Quieres pedir una carta o plantarte? (pedir/plantar): ").lower()
            if action == 'pedir':
                hand.append(deal_card(deck))
                print(f"Mano {i + 1}: {show_hand(hand)}")
                if calculate_hand_value(hand) > 21:
                    print(f"Te has pasado de 21 en la mano {i + 1}. Pierdes ${new_bet}.")
                    balance -= new_bet
                    break
            elif action == 'plantar':
                break

    return split_hands, balance

# Simulación de una partida de Blackjack
def play_blackjack():
    deck = shuffle_deck()
    balance = 100  # Dinero inicial

    while balance > 0:
        bet = place_bet(balance)
        player_hand = []
        dealer_hand = []

        # Repartir dos cartas a cada jugador
        for _ in range(2):
            player_hand.append(deal_card(deck))
            dealer_hand.append(deal_card(deck))

        # Mostrar manos iniciales
        print(f"Mano del jugador: {show_hand(player_hand)}")
        print(f"Mano del dealer: {show_hand(dealer_hand, hidden=True)}")

        # Verificar si el dealer muestra un As para la apuesta segura
        if dealer_hand[0].split()[0] == 'A':
            insurance = insurance_bet(balance, bet)
        else:
            insurance = 0

        # Verificar Blackjack
        if calculate_hand_value(player_hand) == 21:
            if calculate_hand_value(dealer_hand) == 21:
                print(f"Ambos tienen Blackjack. Empate.")
                balance += insurance  # Se devuelve la apuesta segura
            else:
                print(f"¡Blackjack! Ganas ${bet * 1.5}")
                balance += bet * 1.5
            continue

        # Turno del jugador
        while True:
            action = input("¿Quieres pedir una carta, plantarte, dividir, doblar o rendirte? (pedir/plantar/dividir/doblar/rendirse): ").lower()
            if action == 'pedir':
                if len(player_hand) < 11:  # Máximo de 11 cartas
                    player_hand.append(deal_card(deck))
                    print(f"Mano del jugador: {show_hand(player_hand)}")
                    if calculate_hand_value(player_hand) > 21:
                        print(f"Te has pasado de 21. Pierdes ${bet}.")
                        balance -= bet
                        break
                else:
                    print("No puedes pedir más de 9 cartas adicionales.")
            elif action == 'plantar':
                break
            elif action == 'dividir':
                if player_hand[0].split()[0] == player_hand[1].split()[0]:
                    split_hands, balance = split_hand(deck, player_hand, balance, bet)
                    break
                else:
                    print("No puedes dividir, las cartas no son iguales.")
            elif action == 'doblar':
                if len(player_hand) == 2 and calculate_hand_value(player_hand) in [9, 10, 11]:
                    if balance >= bet * 2:
                        bet *= 2
                        player_hand.append(deal_card(deck))
                        print(f"Mano del jugador: {show_hand(player_hand)}")
                        break
                    else:
                        print("No tienes suficiente saldo para doblar.")
                else:
                    print("Solo puedes doblar con un valor de mano de 9, 10 o 11.")
            elif action == 'rendirse':
                print(f"Te has rendido. Pierdes la mitad de tu apuesta: ${bet / 2}.")
                balance -= bet / 2
                break

        player_value = calculate_hand_value(player_hand)
        print(f"Valor final del jugador: {player_value}")

        # Turno del dealer
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card(deck))

        dealer_value = calculate_hand_value(dealer_hand)
        print(f"Mano del dealer: {show_hand(dealer_hand)}")
        print(f"Valor final del dealer: {dealer_value}")

        # Determinar el ganador
        if dealer_value > 21 or player_value > dealer_value:
            print(f"¡El jugador gana ${bet}!")
            balance += bet
        elif dealer_value > player_value:
            print(f"El dealer gana. Pierdes ${bet}.")
            balance -= bet
        else:
            print(f"Empate. Recuperas tu apuesta de ${bet}.")
            balance += insurance  # Se devuelve la apuesta segura

        if balance <= 0:
            print("Te has quedado sin dinero. Gracias por jugar.")
            break
        play_again = input("¿Quieres jugar otra partida? (sí/no): ").lower()
        if play_again != 'sí':
            print(f"Te retiras con ${balance}. Gracias por jugar. ¡Hasta la próxima!")
            break

# Iniciar el juego
play_blackjack()
