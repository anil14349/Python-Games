import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from typing import List, Tuple
import json

class Card:
    COLORS = ['Red', 'Blue', 'Green', 'Yellow']
    NUMBERS = list(range(10))
    SPECIAL_CARDS = ['Skip', 'Reverse', 'Draw Two']
    WILD_CARDS = ['Wild', 'Wild Draw Four']

    def __init__(self, color: str, value: str):
        self.color = color
        self.value = value

    def __str__(self):
        if self.color == 'Wild':
            return self.value
        return f"{self.color} {self.value}"

    def is_playable(self, top_card) -> bool:
        if self.color == 'Wild':
            return True
        if top_card.color == self.color:
            return True
        if isinstance(self.value, str) and self.value == top_card.value:
            return True
        if isinstance(self.value, int) and self.value == top_card.value:
            return True
        return False

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []

    def add_card(self, card: Card):
        self.hand.append(card)

    def remove_card(self, index: int) -> Card:
        return self.hand.pop(index)

    def has_playable_card(self, top_card: Card) -> bool:
        return any(card.is_playable(top_card) for card in self.hand)

class UnoGame:
    def __init__(self):
        self.deck: List[Card] = []
        self.players: List[Player] = []
        self.discard_pile: List[Card] = []
        self.current_player_index = 0
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise
        self.cards_to_draw = 0  # Track accumulated cards to draw
        self.initialize_deck()

    def initialize_deck(self):
        # Add number cards
        for color in Card.COLORS:
            # One 0 card per color
            self.deck.append(Card(color, 0))
            # Two of each number 1-9 per color
            for number in range(1, 10):
                self.deck.extend([Card(color, number) for _ in range(2)])
            # Two of each special card per color
            for special in Card.SPECIAL_CARDS:
                self.deck.extend([Card(color, special) for _ in range(2)])

        # Add wild cards
        for _ in range(4):
            self.deck.append(Card('Wild', 'Wild'))
            self.deck.append(Card('Wild', 'Wild Draw Four'))

        random.shuffle(self.deck)

    def add_player(self, name: str):
        player = Player(name)
        self.players.append(player)
        # Deal 7 cards to the player
        for _ in range(7):
            player.add_card(self.deck.pop())

    def start_game(self):
        # Place first card
        initial_card = self.deck.pop()
        while initial_card.color == 'Wild':
            self.deck.append(initial_card)
            random.shuffle(self.deck)
            initial_card = self.deck.pop()
        self.discard_pile.append(initial_card)

    def get_top_card(self) -> Card:
        return self.discard_pile[-1]

    def reshuffle_if_needed(self, cards_needed: int) -> bool:
        """Reshuffle discard pile into deck if needed and possible"""
        if len(self.deck) >= cards_needed:
            return True
            
        if len(self.discard_pile) <= 1:  # Can't reshuffle if only top card
            return False
            
        # Reshuffle discard pile into deck
        top_card = self.discard_pile.pop()
        self.deck.extend(self.discard_pile)
        self.discard_pile.clear()
        self.discard_pile.append(top_card)
        random.shuffle(self.deck)
        return True

    def handle_special_card(self, card: Card):
        if card.value == 'Skip':
            self.next_player()
        elif card.value == 'Reverse':
            self.direction *= -1
            if len(self.players) == 2:
                self.next_player()
        elif card.value == 'Draw Two':
            self.cards_to_draw += 2
            next_player = self.players[self.get_next_player_index()]
            
            # Check if next player has a Draw Two card
            has_draw_two = any(c.value == 'Draw Two' for c in next_player.hand)
            
            if not has_draw_two:
                # Draw accumulated cards
                cards_needed = self.cards_to_draw
                if not self.reshuffle_if_needed(cards_needed):
                    # If we can't get enough cards, draw what we can
                    cards_needed = len(self.deck)
                
                for _ in range(cards_needed):
                    if self.deck:
                        next_player.add_card(self.deck.pop())
                
                self.cards_to_draw = 0  # Reset accumulated cards
                self.next_player()
            else:
                # Next player might stack another +2
                self.next_player()
                
        elif card.value == 'Wild Draw Four':
            next_player = self.players[self.get_next_player_index()]
            cards_needed = 4
            
            if not self.reshuffle_if_needed(cards_needed):
                # If we can't get enough cards, draw what we can
                cards_needed = len(self.deck)
                
            for _ in range(cards_needed):
                if self.deck:
                    next_player.add_card(self.deck.pop())
            self.next_player()

    def play_card(self, player_index: int, card_index: int, chosen_color: str = None) -> bool:
        player = self.players[player_index]
        card = player.hand[card_index]
        top_card = self.get_top_card()

        # If there are cards to draw, only allow playing a Draw Two card
        if self.cards_to_draw > 0 and card.value != 'Draw Two':
            return False

        if not card.is_playable(top_card):
            return False

        played_card = player.remove_card(card_index)
        if played_card.color == 'Wild':
            played_card.color = chosen_color

        self.discard_pile.append(played_card)
        self.handle_special_card(played_card)
        return True

    def draw_card(self, player_index: int):
        if self.deck:
            self.players[player_index].add_card(self.deck.pop())
        elif len(self.discard_pile) > 1:
            top_card = self.discard_pile.pop()
            self.deck = self.discard_pile
            self.discard_pile = [top_card]
            random.shuffle(self.deck)
            self.players[player_index].add_card(self.deck.pop())

    def next_player(self):
        self.current_player_index = self.get_next_player_index()

    def get_next_player_index(self) -> int:
        return (self.current_player_index + self.direction) % len(self.players)

class UnoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UNO Card Game")
        
        # Define color scheme with lighter colors
        self.colors = {
            'bg': '#f0f2f5',  # Light gray-blue background
            'card_bg': '#ffffff',  # White card background
            'accent': '#4a90e2',  # Bright blue accent
            'button': '#5c6bc0',  # Material indigo
            'button_hover': '#7986cb',  # Lighter indigo
            'text': '#2c3e50',  # Dark blue-gray text
            'highlight': '#e3f2fd',  # Very light blue highlight
            'shadow': '#b0bec5',  # Blue-gray shadow
            'success': '#4caf50',  # Green for success actions
            'warning': '#ff9800'   # Orange for warning actions
        }
        
        # Define common styles
        self.label_style = {
            'bg': self.colors['bg'],
            'fg': self.colors['text'],
            'font': ('Helvetica', 14, 'bold'),
            'pady': 5
        }
        
        self.button_style = {
            'bg': self.colors['button'],
            'fg': 'white',
            'font': ('Helvetica', 12, 'bold'),
            'activebackground': self.colors['button_hover'],
            'activeforeground': 'white',
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 10,
            'width': 10  # Fixed width for consistency
        }
        
        # Initialize game
        self.game = UnoGame()
        self.setup_gui()
        self.start_new_game()

    def setup_gui(self):
        # Create main container with padding
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'], padx=30, pady=30)
        self.main_container.pack(expand=True, fill='both')

        # Game title at the top
        self.title_label = tk.Label(self.main_container, 
                                  text="UNO CARD GAME",
                                  font=('Helvetica', 28, 'bold'),
                                  bg=self.colors['bg'],
                                  fg=self.colors['accent'])
        self.title_label.pack(pady=(0, 30))

        # Top frame for game info and controls
        self.top_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.top_frame.pack(fill='x', pady=(0, 30))

        # Game info with modern styling
        self.info_frame = tk.Frame(self.top_frame, bg=self.colors['card_bg'], 
                                 padx=15, pady=10)
        self.info_frame.pack(side='left')

        self.info_label = tk.Label(self.info_frame,
                                 font=('Helvetica', 16, 'bold'),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text'])
        self.info_label.pack(side='left')

        # Control buttons frame with shadow effect
        self.control_frame = tk.Frame(self.top_frame, bg=self.colors['shadow'],
                                    padx=2, pady=2)
        self.control_frame.pack(side='right')

        # Inner frame for controls
        self.control_inner = tk.Frame(self.control_frame, bg=self.colors['card_bg'],
                                    padx=10, pady=10)
        self.control_inner.pack()

        # New Game button with success color
        self.new_game_button = tk.Button(self.control_inner, 
                                       text="New Game",
                                       command=self.start_new_game,
                                       bg=self.colors['success'],
                                       activebackground='#66bb6a',  # Lighter green
                                       **{k: v for k, v in self.button_style.items() 
                                          if k not in ['bg', 'activebackground']})
        self.new_game_button.pack(side='left', padx=5)

        # Help button with warning color
        self.help_button = tk.Button(self.control_inner, 
                                   text="Rules",
                                   command=self.show_instructions,
                                   bg=self.colors['warning'],
                                   activebackground='#ffb74d',  # Lighter orange
                                   **{k: v for k, v in self.button_style.items() 
                                      if k not in ['bg', 'activebackground']})
        self.help_button.pack(side='left', padx=5)

        # Middle frame for game area
        self.middle_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.middle_frame.pack(expand=True, fill='both', pady=20)

        # Left side for discard pile and deck
        self.game_area = tk.Frame(self.middle_frame, bg=self.colors['bg'])
        self.game_area.pack(side='left', padx=20)

        # Discard pile frame with border
        self.discard_frame = tk.Frame(self.game_area, bg=self.colors['accent'],
                                    padx=2, pady=2)
        self.discard_frame.pack(side='left', padx=30)

        # Create a frame for the draw button with enhanced shadow effect
        self.draw_button_frame = tk.Frame(self.game_area, bg=self.colors['shadow'])
        self.draw_button_frame.pack(side='left', padx=30)
        
        # Inner frame for gradient effect
        self.draw_button_inner = tk.Frame(self.draw_button_frame, 
                                        bg=self.colors['button'],
                                        padx=3, pady=3)
        self.draw_button_inner.pack(padx=3, pady=3)

        # Draw card button with enhanced styling
        self.draw_button = tk.Button(self.draw_button_inner,
                                   text="DRAW\nCARD",
                                   command=self.draw_card,
                                   font=('Helvetica', 18, 'bold'),
                                   bg=self.colors['button'],
                                   fg='white',
                                   activebackground=self.colors['button_hover'],
                                   activeforeground='white',
                                   width=8, height=3,
                                   relief='flat',
                                   cursor='hand2')
        self.draw_button.pack(padx=3, pady=3)
        
        # Add hover effect to draw button
        def on_enter(e):
            self.draw_button.configure(bg=self.colors['button_hover'])
            self.draw_button_inner.configure(bg=self.colors['button_hover'])
            
        def on_leave(e):
            self.draw_button.configure(bg=self.colors['button'])
            self.draw_button_inner.configure(bg=self.colors['button'])
            
        self.draw_button.bind('<Enter>', on_enter)
        self.draw_button.bind('<Leave>', on_leave)

        # Right panel for player's hand
        self.right_panel = tk.Frame(self.middle_frame, bg=self.colors['bg'])
        self.right_panel.pack(side='right', expand=True, fill='both', padx=20)

        # Player's hand label with enhanced styling
        self.hand_label = tk.Label(self.right_panel, 
                                 text="YOUR CARDS",
                                 font=('Helvetica', 20, 'bold'),
                                 bg=self.colors['bg'],
                                 fg=self.colors['accent'])
        self.hand_label.pack(pady=(0, 20))

        # Create scrollable canvas for cards
        self.canvas = tk.Canvas(self.right_panel, bg=self.colors['bg'],
                              highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.right_panel, orient="vertical",
                                    command=self.canvas.yview)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", expand=True, fill="both")
        self.scrollbar.pack(side="right", fill="y")

        # Create frame for cards
        self.card_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        self.canvas_frame = self.canvas.create_window((0, 0),
                                                    window=self.card_frame,
                                                    anchor="nw")

        # Bind canvas configuration
        self.card_frame.bind("<Configure>",
                           lambda e: self.canvas.configure(
                               scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Status bar at the bottom
        self.status_frame = tk.Frame(self.main_container, bg=self.colors['accent'],
                                   height=30)
        self.status_frame.pack(fill='x', pady=(20, 0))
        
        self.status_label = tk.Label(self.status_frame,
                                   text="Welcome to UNO!",
                                   bg=self.colors['accent'],
                                   fg='white',
                                   font=('Helvetica', 10))
        self.status_label.pack(pady=5)

        self.player_cards = []

    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)

    def create_card_display(self, card):
        """Create a formatted display text for the card with improved styling"""
        # Card frame
        border = '╭' + '─' * 12 + '╮\n'
        footer = '╰' + '─' * 12 + '╯'
        
        # Create middle content based on card type
        if isinstance(card.value, int):
            symbol = str(card.value)
            content = f"│    {symbol:^3}    │\n"
        elif card.value in Card.SPECIAL_CARDS:
            symbols = {
                'Skip': '⊘',
                'Reverse': '⟲',
                'Draw Two': '+2'
            }
            symbol = symbols.get(card.value, card.value)
            content = f"│    {symbol:^3}    │\n"
        else:  # Wild cards
            symbol = '+4' if card.value == 'Wild Draw Four' else '★'
            content = f"│    {symbol:^3}    │\n"

        # Create decorative elements
        empty_line = "│            │\n"
        if card.value in Card.SPECIAL_CARDS or card.color == 'Wild':
            decoration = f"│   {'✦' * 3}   │\n"
        else:
            decoration = f"│    {symbol}    │\n"

        # Combine all parts
        return (border + 
                decoration +
                empty_line +
                content +
                empty_line +
                decoration +
                footer)

    def get_card_colors(self, card):
        """Get enhanced colors for cards with gradients and shadows"""
        # Define color schemes with main color, highlight, and shadow
        colors = {
            'Red': {
                'bg': '#FF3333',
                'fg': '#FFFFFF',
                'border': '#CC0000',
                'highlight': '#FF6666',
                'shadow': '#990000'
            },
            'Blue': {
                'bg': '#3333FF',
                'fg': '#FFFFFF',
                'border': '#0000CC',
                'highlight': '#6666FF',
                'shadow': '#000099'
            },
            'Green': {
                'bg': '#33CC33',
                'fg': '#000000',
                'border': '#008800',
                'highlight': '#66FF66',
                'shadow': '#006600'
            },
            'Yellow': {
                'bg': '#FFFF33',
                'fg': '#000000',
                'border': '#CCCC00',
                'highlight': '#FFFF66',
                'shadow': '#999900'
            },
            'Wild': {
                'bg': '#4A4A4A',
                'fg': '#FFFFFF',
                'border': '#2A2A2A',
                'highlight': '#666666',
                'shadow': '#1A1A1A'
            }
        }
        return colors.get(card.color, {
            'bg': '#FFFFFF',
            'fg': '#000000',
            'border': '#CCCCCC',
            'highlight': '#FFFFFF',
            'shadow': '#999999'
        })

    def create_card_button(self, parent, card, command):
        """Create a styled card button with enhanced visual effects"""
        colors = self.get_card_colors(card)
        
        # Create outer frame for shadow effect
        shadow_frame = tk.Frame(parent, bg=colors['shadow'], padx=2, pady=2)
        
        # Create middle frame for border effect
        border_frame = tk.Frame(shadow_frame, bg=colors['border'], padx=1, pady=1)
        border_frame.pack(expand=True, fill='both')
        
        # Create inner frame for highlight effect
        highlight_frame = tk.Frame(border_frame, bg=colors['highlight'], padx=1, pady=1)
        highlight_frame.pack(expand=True, fill='both')
        
        # Create the actual card button
        button = tk.Button(
            highlight_frame,
            text=self.create_card_display(card),
            font=('Helvetica', 12, 'bold'),
            bg=colors['bg'],
            fg=colors['fg'],
            relief='flat',
            borderwidth=0,
            command=command,
            cursor='hand2',  # Change cursor to hand when hovering
            width=14,
            height=7
        )
        button.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Bind hover effects
        def on_enter(e):
            button.configure(bg=colors['highlight'])
            
        def on_leave(e):
            button.configure(bg=colors['bg'])
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        # Add color label
        color_label = tk.Label(
            highlight_frame,
            text=card.color,
            font=('Helvetica', 10),
            bg=colors['border'],
            fg=colors['fg']
        )
        color_label.pack(fill='x')
        
        return shadow_frame

    def update_player_cards(self):
        # Clear existing cards
        for widget in self.card_frame.winfo_children():
            widget.destroy()
        self.player_cards.clear()

        current_player = self.game.players[self.game.current_player_index]
        
        # Calculate dimensions
        num_cards = len(current_player.hand)
        num_columns = 3
        num_rows = (num_cards + num_columns - 1) // num_columns

        # Configure grid weights
        for i in range(num_columns):
            self.card_frame.grid_columnconfigure(i, weight=1, uniform='column')
        for i in range(num_rows):
            self.card_frame.grid_rowconfigure(i, weight=1)

        # Create and grid the cards
        for i, card in enumerate(current_player.hand):
            row = i // num_columns
            col = i % num_columns
            
            # Create card with enhanced styling
            card_container = self.create_card_button(
                self.card_frame,
                card,
                lambda idx=i: self.play_card(idx)
            )
            card_container.grid(
                row=row,
                column=col,
                padx=5,
                pady=5,
                sticky='nsew'
            )
            
            self.player_cards.append(card_container)

        # Update the scroll region
        self.card_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_instructions(self):
        instructions = """
UNO Game Instructions:

Objective:
Be the first player to get rid of all your cards!

Card Types:
• Number Cards (0-9): Match by number or color
• Action Cards:
  ⊘ Skip - Next player loses their turn
  ⇄ Reverse - Changes direction of play
  +2 Draw Two - Next player draws 2 cards
• Wild Cards:
  ★ Wild - Change color to any
  +4 Wild Draw Four - Change color & next player draws 4

How to Play:
1. Match the top card by number or color
2. Play special cards to affect game flow
3. If you can't play, draw a card
4. Say "UNO" when you have one card left!

Click '?' anytime to see these instructions again.
"""
        messagebox.showinfo("How to Play UNO", instructions)

    def start_new_game(self):
        num_players = simpledialog.askinteger("Players", "Enter number of players (2-4):",
                                            minvalue=2, maxvalue=4)
        if not num_players:
            self.root.quit()
            return

        for i in range(num_players):
            name = simpledialog.askstring("Name", f"Enter name for Player {i+1}:")
            if not name:
                name = f"Player {i+1}"
            self.game.add_player(name)

        self.game.start_game()
        self.update_display()

    def update_display(self):
        # Update info label
        current_player = self.game.players[self.game.current_player_index]
        self.info_label.config(text=f"{current_player.name}'s turn")

        # Update top card with styled display
        self.update_top_card()

        # Update player's hand
        self.update_player_cards()

    def update_top_card(self):
        top_card = self.game.get_top_card()
        colors = self.get_card_colors(top_card)
        
        # Create a frame for the top card with border
        if not hasattr(self, 'top_card_frame'):
            self.top_card_frame = tk.Frame(
                self.discard_frame,
                bg=colors['shadow'],
                padx=2,
                pady=2
            )
            self.top_card_frame.pack()
            
            # Create border frame
            self.top_card_border = tk.Frame(
                self.top_card_frame,
                bg=colors['border'],
                padx=1,
                pady=1
            )
            self.top_card_border.pack(expand=True, fill='both')
            
            # Create highlight frame
            self.top_card_highlight = tk.Frame(
                self.top_card_border,
                bg=colors['highlight'],
                padx=1,
                pady=1
            )
            self.top_card_highlight.pack(expand=True, fill='both')
            
            # Create the card label
            self.top_card_label = tk.Label(
                self.top_card_highlight,
                font=('Helvetica', 18, 'bold'),
                relief='flat',
                padx=20,
                pady=10
            )
            self.top_card_label.pack()
            
            # Create the color label
            self.top_card_color_label = tk.Label(
                self.top_card_highlight,
                font=('Helvetica', 12, 'bold')
            )
            self.top_card_color_label.pack(fill='x')

        # Update the card display
        self.top_card_frame.configure(bg=colors['shadow'])
        self.top_card_border.configure(bg=colors['border'])
        self.top_card_highlight.configure(bg=colors['highlight'])
        self.top_card_label.configure(
            text=self.create_card_display(top_card),
            bg=colors['bg'],
            fg=colors['fg']
        )
        self.top_card_color_label.configure(
            text=top_card.color,
            bg=colors['border'],
            fg=colors['fg']
        )

    def play_card(self, card_index):
        current_player = self.game.players[self.game.current_player_index]
        card = current_player.hand[card_index]
        
        if card.color == 'Wild':
            color = self.choose_color()
            if not color:
                return
            if self.game.play_card(self.game.current_player_index, card_index, color):
                if len(current_player.hand) == 0:
                    messagebox.showinfo("Winner!", f"{current_player.name} wins!")
                    self.start_new_game()
                else:
                    self.game.next_player()
                    self.update_display()
        else:
            if self.game.play_card(self.game.current_player_index, card_index):
                if len(current_player.hand) == 0:
                    messagebox.showinfo("Winner!", f"{current_player.name} wins!")
                    self.start_new_game()
                else:
                    self.game.next_player()
                    self.update_display()
            else:
                messagebox.showerror("Invalid Move", "This card cannot be played!")

    def draw_card(self):
        self.game.draw_card(self.game.current_player_index)
        current_player = self.game.players[self.game.current_player_index]
        
        if not current_player.has_playable_card(self.game.get_top_card()):
            messagebox.showinfo("No Playable Cards", 
                              "No playable cards, moving to next player")
            self.game.next_player()
        
        self.update_display()

    def choose_color(self):
        colors = ['Red', 'Blue', 'Green', 'Yellow']
        while True:
            color = simpledialog.askstring("Choose Color",
                                       "Enter color (Red/Blue/Green/Yellow):")
            if color is None:  # User clicked Cancel
                return None
            color = color.strip().capitalize()
            if color in colors:
                return color
            messagebox.showerror("Invalid Color", 
                              f"Please choose from: {', '.join(colors)}")

    def on_canvas_configure(self, event):
        # Update the canvas window width when the canvas is resized
        width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=width)

def main():
    root = tk.Tk()
    game = UnoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
