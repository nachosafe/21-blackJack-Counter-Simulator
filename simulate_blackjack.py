import blackjack  # Asegurando que el archivo blackjack.py se llama así

def adjust_bet(true_count, base_bet):
    if true_count >= 1:
        return base_bet * (true_count + 1)  # Incrementa la apuesta basada en el conteo verdadero
    else:
        return base_bet  # Apuesta base cuando el conteo verdadero es bajo o negativo

def simulate_blackjack(num_games, starting_bankroll, base_bet):
    bankroll = starting_bankroll
    for _ in range(num_games):
        true_count = blackjack.get_true_count()
        bet_amount = adjust_bet(true_count, base_bet)
        result = blackjack.play_game(bet_amount)
        bankroll += result
    return bankroll

if __name__ == "__main__":
    num_games = 10000  # Número de partidas
    starting_bankroll = 1000  # Banca inicial
    base_bet = 10  # Apuesta base por partida
    
    final_bankroll = simulate_blackjack(num_games, starting_bankroll, base_bet)
    print(f"Después de {num_games} partidas, tu banca es: ${final_bankroll}")
