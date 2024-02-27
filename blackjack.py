# Import random and JSON modules.
# The random module will be used for shuffling the deck of cards.
# The JSON module will be used for file handling to save and load the game state.
# The namedtuple module will be used for referring to values using descriptive field names instead of integer indices.
import random
import json
from collections import namedtuple

# Key definitions for JSON
TOTAL_GAMES = "total_games"
TOTAL_WINS = "total_wins"
TOTAL_LOSSES = "total_losses"
TOTAL_TIES = "total_ties"
PLAYER_BUSTS = "player_busts"
DEALER_BUSTS = "dealer_busts"

# Define the named tuple: use suit and rank.
Card = namedtuple('Card', ['suit', 'rank'])

def load_game_stats():
    """
    This function attempts to load game statistics from the file 'game_stats.json'. 
    If the file is not found (FileNotFoundError), it prints a message 
    and returns a default set of statistics with initial values (all 0).
    """
    try:
        with open('game_stats.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {TOTAL_GAMES: 0, TOTAL_WINS: 0, TOTAL_LOSSES: 0, TOTAL_TIES: 0, PLAYER_BUSTS: 0, DEALER_BUSTS: 0}

def save_game_stats(stats):
    """
    This function saves the game statistics to the 'game_stats.json' file.
    """
    try:
        with open('game_stats.json', 'w') as file:
            json.dump(stats, file)
    except FileNotFoundError:
        # If the file is not found, create it and save the stats
        with open('game_stats.json', 'x') as file:
            json.dump(stats, file)

def display_game_stats(stats):
    """
    This function prints the game statistics to the console in a readable format.
    """
    print("\n--- Saved Game Statistics ----\n")
    print(f"Total Games Played: {stats[TOTAL_GAMES]}")
    print(f"Total Wins: {stats[TOTAL_WINS]}")
    print(f"Total Losses: {stats[TOTAL_LOSSES]}")
    print(f"Total Ties: {stats[TOTAL_TIES]}")
    print(f"Player Busts: {stats[PLAYER_BUSTS]}")
    print(f"Dealer Busts: {stats[DEALER_BUSTS]}")
    print("-------------------------------\n")
    
def welcome():
    """
    This function is used to display the contents of the welcome.txt file, 
    which contains a welcome message and general instructions about
    how to play the game.
    """
    try:
        with open('welcome.txt', 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("File 'welcome.txt' not found. Proceeding with the game...")

def create_deck():
    """
    This function generates a standard deck of playing cards.
    The suits (list) represent the four suits (Hearts, Diamonds, Clubs and Spades).
    The ranks (list) represent the ranks of the playing cards (2-10, Jack, Queen, King and Ace).
    The deck is created using a list comprehension.
    The deck is a list of tuples with each card in the form of (suit, rank).
    """
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [Card(suit, rank) for suit in suits for rank in ranks]
    return deck

def shuffle_deck(deck):
    """
    This function takes a deck (a list of cards) and shuffles the items randomly.
    This function is called when initializing a new deck to ensure that the cards
    are in random order before dealing them to the players.
    """
    random.shuffle(deck)

def deal_card(deck):
    """
    This function deals a card from the deck.
    The function takes an argument, which is assumed to be a list representing a deck of cards.
    The function checks if the current deck is empty.
    If yes, it creates a new deck and shuffles it.
    The pop() function draws a card from the top of the deck and removes it from the deck.
    """
    if not deck:
        # Create a new deck if the current one is empty.
        deck = create_deck()
        shuffle_deck(deck)

    # Deal a card from the deck.
    return deck.pop()

def calculate_hand(hand):
    """
    This function determines the total value of a hand.
    The hand is represented as a list of cards.
    The function calculates the total value by summing the values of the individual cards,
    considering the special rules for the Ace (A) card.
    The dictionary maps the card ranks to the their corresponding numerical values.

    The special rules for handing Aces:
    - the Ace can have a value of 11 or 1
    - if counting Ace as 11 would cause a bust (total greater than 21), the Ace is counted as 1 
    """
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    # Calculate the total number of aces in the hand using a generator expression.
    # Check the cards in the hand and add one to the sum if the card is Ace.
    num_aces = sum(1 for card in hand if card.rank == 'A')
    # Calculate the total value of the hand referring to the dictionary,
    # which contains the numerical values associated with each card rank. 
    total = sum(values[card.rank] for card in hand)

    # As long as the total value of the hand is greater than 21 and there are Aces in the hand,
    # the total is recalculated by subtracting 10 for each Ace in the hand.
    while total > 21 and num_aces:
        total -= 10    # -10 to adjust the value of Ace (from 11 to 1)
        num_aces -= 1  # Reduce the number of aces by 1

    return total

def display_hand(hand, show_all=True):
    """
    This function displays the cards with the suits as Unicode symbols.
    The dictionary maps each suit to its corresponding Unicode symbol.
    The function extracts the rank and suit values for each card.
    The suit is converted to its Unicode symbol by referencing it with the get() method.
    The card information is displayed in the format [suit, rank] using an f-string.
    The 'show_all' parameter provides an option to hide the dealer's second card. 
    """
    # Define Unicode symbols for each suit
    suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

    # Show the first card with suit as Unicode symbol.
    print(f"[{suit_symbols.get(hand[0].suit)}{hand[0].rank}]")

    # If show_all is True, print all cards.
    # Otherwise, hide the second card.
    if show_all:
        for card in hand[1:]:
            rank = card.rank
            suit = card.suit
            suit_unicode = suit_symbols.get(suit)
            print(f"[{suit_unicode}{rank}]")
        return

    # Hide the second card, print [X] instead.
    print("[X]")

def first_hand(player, dealer):
    """
    This function displays the initial two cards for the player and dealer, 
    hiding the dealer's second card.
    """
    current_total = calculate_hand(player)
    print(f"Player's hand ({current_total}):")
    display_hand(player)
    print() # Print an empty line.

    print("Dealer's hand (X):")
    display_hand(dealer, show_all=False)
    print() # Print an empty line.

def play_again():
    """
    This function asks if the player wants to continue to play or end the game.
    """
    while True:
        answer = input("Enter [P] to play again or [Q] to quit: ")
        if answer.upper() == 'P':
            print() # Print an empty line.
            break
        elif answer.upper() == 'Q':
            quit()
        else:
            print("Invalid input!\n")

def main():
    welcome()

    game_stats = load_game_stats()

    display_game_stats(game_stats)

    print("LET'S PLAY!\n")

    # This variable holds the total value for the player's hand.
    # Reset the player's hand value to 0 at the start of each round.
    player_total = 0

    # Create the deck of cards.
    cards = create_deck()

    # Shuffle the deck of cards.
    shuffle_deck(cards)

    while True:
        # Counter for the total number of games.
        # +1 every time a new game is started.
        game_stats['total_games'] += 1

        # Define the player and dealer hands.
        player_hand = []
        dealer_hand = []

        # Define a flag for bust (True) or not bust (False).
        # This flag is used to go directly to a new game or quit (play_again),
        # if the player goes bust.
        # There is no need to play the dealer's hand in this case.
        # Set the flag to False with a new hand.
        bust = False

        # Deal the player and dealer's initial cards.
        for _ in range(2):
            player_hand.append(deal_card(cards))
            dealer_hand.append(deal_card(cards))

        first_hand(player_hand, dealer_hand)

        # Player's turn
        while True:
            action = input("Enter [H] to hit or [S] to stand: ")
            print() # Print an empty line.
            # If the player chooses to hit (H),
            # add a new card to the current hand
            # and calculate the new hand total.
            if action.upper() == 'H':
                player_hand.append(deal_card(cards))
                player_total = calculate_hand(player_hand)
                print(f"Player's hand ({player_total}):")
                display_hand(player_hand)
                print() # Print an empty line.
                # If the player goes bust,
                # set the bust flag to True
                # and update the game stats values.
                # Show the dealer's hand and value.
                # Then break from the loop.
                if player_total > 21:
                    bust = True
                    game_stats['player_busts'] += 1
                    game_stats['total_losses'] += 1
                    dealer_total = calculate_hand(dealer_hand)
                    print(f"Dealer's hand ({dealer_total}):")
                    display_hand(dealer_hand)
                    print() # Print an empty line.
                    print("RESULT: Bust! You lose.\n")
                    break
            # If the player chooses to stand (S),
            # break from the loop and move to the dealer's turn.
            elif action.upper() == 'S':
                break
            else:
                print("Invalid input!\n")  

        # Dealer's turn
        if not bust:
            dealer_total = calculate_hand(dealer_hand)
            print(f"Dealer's hand ({dealer_total}):")
            display_hand(dealer_hand)
            print() # Print an empty line.

            while calculate_hand(dealer_hand) < 17:
                print("The dealer takes a new card!\n")
                dealer_hand.append(deal_card(cards))
                dealer_total = calculate_hand(dealer_hand)
                print(f"Dealer's hand ({dealer_total}):")
                display_hand(dealer_hand)
                print() # Print an empty line.
                if dealer_total > 21:
                    game_stats['dealer_busts'] += 1
                    game_stats['total_wins'] += 1
                    print("RESULT: The dealer bust. You win!\n")
                    break
                    
        # Calculate the final total hand values for the player and the dealer. 
        player_total = calculate_hand(player_hand)
        dealer_total = calculate_hand(dealer_hand)

        scores = f"SCORES: Player ({player_total}), Dealer ({dealer_total})"

        # Checking the result.
        # Going bust (over 21) is checked in the earlier while loops.
        # The conditionals must include a constrait for 
        # the player_total and dealer_total to be less than or equal to 21.
        # Otherwise, the game logic can falsely indicate a bust result as a win.
        if player_total == dealer_total:
            game_stats['total_ties'] += 1
            print(scores)
            print("RESULT: It's a tie!\n")
        elif player_total > dealer_total and player_total <= 21:
            game_stats['total_wins'] += 1
            print(scores)
            print("RESULT: You win!\n")
        elif dealer_total > player_total and dealer_total <= 21:
            game_stats['total_losses'] += 1
            print(scores)
            print("RESULT: You lose! The dealer wins.\n")

        save_game_stats(game_stats)

        # Ask the user to play again or end the game.
        play_again()

if __name__ == "__main__":
    main()
