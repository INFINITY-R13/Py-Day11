import random
import tkinter as tk
from collections import defaultdict

class BlackjackGUI:
    """
    A refined GUI for a game of Blackjack using Tkinter.

    This version improves on the original by:
    - Adding color to the cards for better visual distinction.
    - Enhancing the UI with a more modern and clean layout.
    - Removing the popup message box for a smoother end-game experience.
    """
    # Class attribute for card values, accessible by all methods.
    CARD_VALUES = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                   '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
    
    # Card suits and colors
    SUITS = {'♠': 'black', '♣': 'black', '♥': 'red', '♦': 'red'}


    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        self.root.configure(bg="#013220") # Dark green background

        self.deck = []
        self.stats = defaultdict(int)
        self.user_cards = []
        self.computer_cards = []
        self.is_game_over = True # Game starts as "over" until "New Game" is pressed

        self.setup_gui()
        self.update_stats_display()

    def create_deck(self):
        """Create a standard deck of 52 cards with suits and shuffle it."""
        self.deck = [(rank, suit) for suit in self.SUITS for rank in self.CARD_VALUES]
        random.shuffle(self.deck)

    def deal_card(self):
        """Deal a card from the deck, reshuffle if empty."""
        if not self.deck:
            self.create_deck()
        return self.deck.pop()

    def calculate_score(self, cards):
        """
        Calculate the score of a hand, handling Aces optimally.
        A Blackjack (21 on the first two cards) is represented by a score of 0.
        """
        score = sum(self.CARD_VALUES[rank] for rank, _ in cards)
        num_aces = sum(1 for rank, _ in cards if rank == 'A')

        # Adjust for Aces: if score is over 21, change Ace value from 11 to 1.
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        
        # A score of 0 represents a Blackjack
        if score == 21 and len(cards) == 2:
            return 0
        return score

    def compare(self, user_score, computer_score):
        """Compare user and computer scores to determine the outcome."""
        if user_score == computer_score:
            return 'Draw', "It's a Draw"
        elif computer_score == 0:
            return 'Lose', 'Computer has Blackjack. You lose.'
        elif user_score == 0:
            return 'Win', 'Blackjack! You win!'
        elif user_score > 21:
            return 'Lose', 'You went over 21. You lose.'
        elif computer_score > 21:
            return 'Win', 'Computer went over 21. You win!'
        elif user_score > computer_score:
            return 'Win', 'You win!'
        else:
            return 'Lose', 'You lose.'

    def setup_gui(self):
        """Set up the Tkinter GUI layout with a modern casino theme."""
        # Main container
        container = tk.Frame(self.root, bg="#013220")
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # Title Label
        title_label = tk.Label(container, text="Blackjack", font=("Helvetica", 32, "bold"), bg="#013220", fg="white")
        title_label.pack(pady=(10, 20))

        # Result display
        self.result_label = tk.Label(container, text="Press 'New Game' to begin!", font=("Helvetica", 18, "italic"), bg="#013220", fg="#FFD700")
        self.result_label.pack(pady=20)

        # Game table frame
        table_frame = tk.Frame(container, bg="#014421")
        table_frame.pack(expand=True, fill="both", padx=20)
        table_frame.columnconfigure(0, weight=1)
        table_frame.columnconfigure(1, weight=1)

        # Player's area
        self.user_frame = tk.LabelFrame(table_frame, text="Your Hand", font=("Helvetica", 14), bg="#014421", fg="white", bd=2, relief="groove", padx=10, pady=10)
        self.user_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.user_score_label = tk.Label(self.user_frame, text="Score: 0", font=("Helvetica", 16, "bold"), bg="#014421", fg="white")
        self.user_score_label.pack(pady=5)
        self.user_cards_frame = tk.Frame(self.user_frame, bg="#014421")
        self.user_cards_frame.pack(pady=10, expand=True)

        # Computer's area
        self.computer_frame = tk.LabelFrame(table_frame, text="Computer's Hand", font=("Helvetica", 14), bg="#014421", fg="white", bd=2, relief="groove", padx=10, pady=10)
        self.computer_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.computer_score_label = tk.Label(self.computer_frame, text="Score: ?", font=("Helvetica", 16, "bold"), bg="#014421", fg="white")
        self.computer_score_label.pack(pady=5)
        self.computer_cards_frame = tk.Frame(self.computer_frame, bg="#014421")
        self.computer_cards_frame.pack(pady=10, expand=True)

        # Stats label
        self.stats_label = tk.Label(container, text="", font=("Helvetica", 12), bg="#013220", fg="white")
        self.stats_label.pack(pady=10)

        # Buttons frame
        button_frame = tk.Frame(container, bg="#013220")
        button_frame.pack(pady=20)

        button_style = {"font": ("Helvetica", 12, "bold"), "bg": "#FFD700", "fg": "black", 
                        "activebackground": "#FFEC8B", "activeforeground": "black", "padx": 20, "pady": 10, "relief": "raised", "bd": 2}

        self.new_game_button = tk.Button(button_frame, text="New Game", command=self.start_game, **button_style)
        self.new_game_button.grid(row=0, column=0, padx=10)
        self.hit_button = tk.Button(button_frame, text="Hit", command=self.hit, state=tk.DISABLED, **button_style)
        self.hit_button.grid(row=0, column=1, padx=10)
        self.stand_button = tk.Button(button_frame, text="Stand", command=self.stand, state=tk.DISABLED, **button_style)
        self.stand_button.grid(row=0, column=2, padx=10)

    def display_cards(self, frame, cards, hide_first=False):
        """Creates stylish labels for each card and displays them."""
        for widget in frame.winfo_children():
            widget.destroy()
        
        for i, (rank, suit) in enumerate(cards):
            if hide_first and i == 0:
                card_text = "?\n?"
                card_color = "gray"
            else:
                card_text = f"{rank}\n{suit}"
                card_color = self.SUITS[suit]

            card_label = tk.Label(frame, text=card_text, font=("Courier", 20, "bold"), 
                                  bg="white", fg=card_color, relief="solid", borderwidth=1, width=4, height=2)
            card_label.pack(side="left", padx=5, pady=5)


    def update_displays(self, show_computer_full_hand=False):
        """Update the GUI with the current game state."""
        user_score = self.calculate_score(self.user_cards)
        self.display_cards(self.user_cards_frame, self.user_cards)
        self.user_score_label.config(text=f"Score: {user_score if user_score != 0 else 'Blackjack!'}")
        
        if show_computer_full_hand:
            computer_score = self.calculate_score(self.computer_cards)
            self.display_cards(self.computer_cards_frame, self.computer_cards)
            self.computer_score_label.config(text=f"Score: {computer_score if computer_score != 0 else 'Blackjack!'}")
        else:
            self.display_cards(self.computer_cards_frame, self.computer_cards, hide_first=True)
            self.computer_score_label.config(text="Score: ?")

    def update_stats_display(self):
        self.stats_label.config(text=f"Wins: {self.stats['Win']} | Losses: {self.stats['Lose']} | Draws: {self.stats['Draw']}")

    def start_game(self):
        """Start a new game of Blackjack."""
        self.create_deck()
        self.user_cards = [self.deal_card() for _ in range(2)]
        self.computer_cards = [self.deal_card() for _ in range(2)]
        self.is_game_over = False

        self.result_label.config(text="")
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        
        self.update_displays()
        
        user_score = self.calculate_score(self.user_cards)
        if user_score == 0: # Automatic win on Blackjack
            self.stand()

    def hit(self):
        """Player requests another card."""
        if not self.is_game_over:
            self.user_cards.append(self.deal_card())
            self.update_displays()
            user_score = self.calculate_score(self.user_cards)
            if user_score >= 21: # End turn on 21 or bust
                self.stand()

    def stand(self):
        """Player ends their turn, computer plays."""
        if not self.is_game_over:
            self.is_game_over = True
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.end_game()

    def end_game(self):
        """Conclude the game, reveal cards, and determine the winner."""
        # Computer's turn logic: hit until score is 17 or more.
        computer_score = self.calculate_score(self.computer_cards)
        while computer_score != 0 and computer_score < 17:
            self.computer_cards.append(self.deal_card())
            computer_score = self.calculate_score(self.computer_cards)
        
        user_score = self.calculate_score(self.user_cards)
        result, message = self.compare(user_score, computer_score)
        self.stats[result] += 1
        
        self.update_displays(show_computer_full_hand=True)
        self.update_stats_display()
        self.result_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
