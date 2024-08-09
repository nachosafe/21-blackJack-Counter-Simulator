import blackjack  # Asumiendo que el archivo blackjack.py se llama así

def simulate_blackjack(num_games, starting_bankroll, bet_amount):
    bankroll = starting_bankroll
    for _ in range(num_games):
        result = blackjack.play_game(bet_amount)  # Esta función debería retornar el resultado del juego
        bankroll += result  # Suma o resta según el resultado
    
    return bankroll

if __name__ == "__main__":
    num_games = 100000  # Número de partidas
    starting_bankroll = 1000  # Banca inicial
    bet_amount = 10  # Apuesta constante por partida
    
    final_bankroll = simulate_blackjack(num_games, starting_bankroll, bet_amount)
    print(f"Después de {num_games} partidas, tu banca es: ${final_bankroll}")
