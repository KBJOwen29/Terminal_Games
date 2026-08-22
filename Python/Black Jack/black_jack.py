import random


# Create a deck of cards
def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = [
        "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "J", "Q", "K", "A"
    ]

    deck = []

    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck


# Get the value of a card
def card_value(card):
    rank = card[0]

    if rank in ["J", "Q", "K"]:
        return 10

    if rank == "A":
        return 11

    return int(rank)


# Calculate the total value of a hand
def calculate_score(hand):
    score = 0
    aces = 0

    for card in hand:
        score += card_value(card)

        if card[0] == "A":
            aces += 1

    # Convert Ace from 11 to 1 when necessary
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score


# Display cards
def display_hand(name, hand, hide_first_card=False):
    print(f"\n{name}:")

    for i, card in enumerate(hand):
        if hide_first_card and i == 0:
            print("  Hidden Card")
        else:
            print(f"  {card[0]} of {card[1]}")

    if not hide_first_card:
        print(f"Score: {calculate_score(hand)}")


# Play one round
def play_game():
    deck = create_deck()

    player_hand = [
        deck.pop(),
        deck.pop()
    ]

    dealer_hand = [
        deck.pop(),
        deck.pop()
    ]

    print("\n========== BLACKJACK ==========")

    display_hand("Dealer", dealer_hand, hide_first_card=True)
    display_hand("Player", player_hand)

    # Check for immediate Blackjack
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score == 21:
        display_hand("Dealer", dealer_hand)

        if dealer_score == 21:
            print("\nBoth players have Blackjack!")
        else:
            print("\nBLACKJACK! You win!")

        return

    if dealer_score == 21:
        display_hand("Dealer", dealer_hand)
        print("\nDealer has Blackjack! You lose!")
        return

    # Player's turn
    while True:
        player_score = calculate_score(player_hand)

        if player_score > 21:
            print("\nYou busted!")
            return

        print("\nWhat do you want to do?")
        print("1. Hit")
        print("2. Stand")

        choice = input("Choose: ")

        if choice == "1":
            new_card = deck.pop()
            player_hand.append(new_card)

            print(f"\nYou drew: {new_card[0]} of {new_card[1]}")
            display_hand("Player", player_hand)

        elif choice == "2":
            break

        else:
            print("Invalid choice.")

    # Dealer's turn
    print("\n========== DEALER'S TURN ==========")

    display_hand("Dealer", dealer_hand)

    while calculate_score(dealer_hand) < 17:
        new_card = deck.pop()
        dealer_hand.append(new_card)

        print(
            f"Dealer draws: "
            f"{new_card[0]} of {new_card[1]}"
        )

        display_hand("Dealer", dealer_hand)

    dealer_score = calculate_score(dealer_hand)
    player_score = calculate_score(player_hand)

    # Determine winner
    print("\n========== RESULT ==========")

    if dealer_score > 21:
        print("Dealer busted!")
        print("You win!")

    elif player_score > dealer_score:
        print("You win!")

    elif player_score < dealer_score:
        print("Dealer wins!")

    else:
        print("It's a draw!")


# Main program
while True:
    play_game()

    print("\nPlay again?")
    choice = input("Enter Y/N: ").lower()

    if choice != "y":
        print("\nThanks for playing Blackjack!")
        break
