import random
import os

def deal_card():
    """Returns a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """Take a list of cards and return the calculated score."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(u_score, c_score):
    """Compare the user and computer scores."""
    if u_score == c_score:
        return 'Draw'
    elif c_score == 0:
        return 'Lose, Computer has a blackjack'
    elif u_score == 0:
        return 'Win with a blackjack'
    elif c_score > 21:
        return 'Computer went over. You Win'
    elif u_score > 21:
        return 'You went over. Computer wins'
    elif u_score > c_score:
        return 'You Win'
    else:
        return 'You Lose'
    
def play_game():
    user_cards = []
    computer_cards = []
    is_game_over = False

    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        print(f"Your cards: {user_cards}")
        print(f"Current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}")

        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            user_should_deal = input("Type 'y' to get another card, type 'n' to pass: ").lower()
            if user_should_deal == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True    

    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card()) 
        computer_score = calculate_score(computer_cards)           

    print(f"Your final hand: {user_cards}, final score: {user_score}")
    print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score))

while input("Do you want to play a game of blackjack? Type 'y' or 'n': ").lower() == 'y':
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    play_game()
