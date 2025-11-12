import random


# Création du deck
def create_deck():
    suits = ['Coeur', 'Carreau', 'Trèfle', 'Pique']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
    deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


# Calcul de la valeur d'une main
def hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        if card['rank'] in ['Valet', 'Dame', 'Roi']:
            value += 10
        elif card['rank'] == 'As':
            value += 11
            ace_count += 1
        else:
            value += int(card['rank'])
    # Ajuster les As si nécessaire
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    return value


# Affichage de la main
def display_hand(hand, player_name, hide_first_card=False):
    print(f"{player_name} a : ", end='')
    for i, card in enumerate(hand):
        if i == 0 and hide_first_card:
            print("[cachée]", end=' ')
        else:
            print(f"{card['rank']} de {card['suit']}", end=' ')
    print()


# Jeu principal
def blackjack():
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Tour du joueur
    while True:
        display_hand(player_hand, "Joueur")
        display_hand(dealer_hand, "Croupier", hide_first_card=True)
        if hand_value(player_hand) == 21:
            print("Blackjack! 🎉")
            break
        choice = input("Voulez-vous tirer une carte (t) ou rester (r) ? ").lower()
        if choice == 't':
            player_hand.append(deck.pop())
            if hand_value(player_hand) > 21:
                display_hand(player_hand, "Joueur")
                print("Vous avez dépassé 21! Vous perdez 😢")
                return
        elif choice == 'r':
            break

    # Tour du croupier
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    display_hand(dealer_hand, "Croupier")

    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    print(f"Total joueur : {player_total}")
    print(f"Total croupier : {dealer_total}")

    if dealer_total > 21 or player_total > dealer_total:
        print("Vous gagnez! 🎉")
    elif player_total < dealer_total:
        print("Vous perdez 😢")
    else:
        print("Égalité 🤝")


# Lancer le jeu
if __name__ == "__main__":
    blackjack()
