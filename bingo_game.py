import tkinter as tk
from tkinter import messagebox
import random

class BingoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Game")
        
        # Define color scheme
        self.colors = {
            'bg': '#f0f2f5',  # Light gray-blue background
            'card_bg': '#ffffff',  # White card background
            'accent': '#4a90e2',  # Bright blue accent
            'button': '#5c6bc0',  # Material indigo
            'button_hover': '#7986cb',  # Lighter indigo
            'text': '#2c3e50',  # Dark blue-gray text
            'marked': '#4caf50',  # Green for marked numbers
            'highlight': '#e3f2fd',  # Very light blue highlight
            'shadow': '#b0bec5'  # Blue-gray shadow
        }
        
        # Game state
        self.numbers = []
        self.marked = set()
        self.bingo_count = 0
        self.game_over = False
        
        self.setup_gui()
        self.new_game()
    
    def setup_gui(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'], padx=30, pady=30)
        self.main_container.pack(expand=True, fill='both')
        
        # Title
        self.title_label = tk.Label(
            self.main_container,
            text="BINGO",
            font=('Helvetica', 36, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.title_label.pack(pady=(0, 30))
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.control_frame.pack(fill='x', pady=(0, 20))
        
        # New Game button
        self.new_game_btn = tk.Button(
            self.control_frame,
            text="New Game",
            command=self.new_game,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['button'],
            fg='white',
            activebackground=self.colors['button_hover'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10
        )
        self.new_game_btn.pack(side='left', padx=5)
        
        # Bingo progress
        self.bingo_label = tk.Label(
            self.control_frame,
            text="BINGO: ",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.bingo_label.pack(side='right', padx=5)
        
        # Game board frame with shadow effect
        self.board_outer = tk.Frame(
            self.main_container,
            bg=self.colors['shadow'],
            padx=2,
            pady=2
        )
        self.board_outer.pack(expand=True, padx=20, pady=20)
        
        # Inner board frame
        self.board_frame = tk.Frame(
            self.board_outer,
            bg=self.colors['card_bg'],
            padx=15,
            pady=15
        )
        self.board_frame.pack(expand=True)
        
        # Create 5x5 grid of buttons
        self.buttons = []
        for i in range(5):
            row = []
            for j in range(5):
                btn = tk.Button(
                    self.board_frame,
                    width=4,
                    height=2,
                    font=('Helvetica', 14, 'bold'),
                    relief='flat',
                    cursor='hand2'
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                btn.configure(command=lambda x=i, y=j: self.mark_number(x, y))
                row.append(btn)
            self.buttons.append(row)
    
    def new_game(self):
        # Reset game state
        self.numbers = random.sample(range(1, 26), 25)
        self.marked = set()
        self.bingo_count = 0
        self.game_over = False
        
        # Update buttons
        for i in range(5):
            for j in range(5):
                num = self.numbers[i * 5 + j]
                btn = self.buttons[i][j]
                btn.configure(
                    text=str(num),
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    state='normal'
                )
        
        # Reset bingo label
        self.update_bingo_display()
    
    def mark_number(self, row, col):
        if self.game_over:
            return
            
        btn = self.buttons[row][col]
        num = self.numbers[row * 5 + col]
        
        if num not in self.marked:
            self.marked.add(num)
            btn.configure(
                bg=self.colors['marked'],
                fg='white'
            )
            self.check_bingo()
    
    def check_bingo(self):
        bingo_count = 0
        
        # Check rows
        for i in range(5):
            if all(self.numbers[i * 5 + j] in self.marked for j in range(5)):
                bingo_count += 1
        
        # Check columns
        for j in range(5):
            if all(self.numbers[i * 5 + j] in self.marked for i in range(5)):
                bingo_count += 1
        
        # Check diagonals
        if all(self.numbers[i * 5 + i] in self.marked for i in range(5)):
            bingo_count += 1
        if all(self.numbers[i * 5 + (4 - i)] in self.marked for i in range(5)):
            bingo_count += 1
        
        self.bingo_count = bingo_count
        self.update_bingo_display()
        
        # Check for win
        if bingo_count >= 5:
            self.game_over = True
            messagebox.showinfo("Congratulations!", "BINGO! You've won the game!")
    
    def update_bingo_display(self):
        display = "BINGO: " + "■" * self.bingo_count + "□" * (5 - self.bingo_count)
        self.bingo_label.configure(text=display)

if __name__ == "__main__":
    root = tk.Tk()
    game = BingoGame(root)
    root.mainloop()
