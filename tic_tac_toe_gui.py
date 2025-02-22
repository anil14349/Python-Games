import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        
        # Configure style
        self.root.configure(bg='#2C3E50')
        self.root.resizable(False, False)
        
        # Title
        title_frame = tk.Frame(root, bg='#2C3E50')
        title_frame.pack(pady=10)
        title_label = tk.Label(title_frame, text="Tic Tac Toe", 
                             font=('Helvetica', 24, 'bold'),
                             fg='#ECF0F1', bg='#2C3E50')
        title_label.pack()

        # Player turn label
        self.turn_label = tk.Label(root, 
                                 text="Player X's Turn",
                                 font=('Helvetica', 16),
                                 fg='#ECF0F1', bg='#2C3E50')
        self.turn_label.pack(pady=5)

        # Game board
        self.game_frame = tk.Frame(root, bg='#2C3E50')
        self.game_frame.pack(padx=10, pady=10)

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, 
                                 text="",
                                 font=('Helvetica', 20, 'bold'),
                                 width=5, height=2,
                                 bg='#34495E',
                                 fg='#ECF0F1',
                                 activebackground='#2980B9',
                                 relief=tk.RAISED,
                                 command=lambda row=i, col=j: 
                                     self.button_click(row, col))
                button.grid(row=i, column=j, padx=3, pady=3)
                self.buttons.append(button)

        # Reset button
        reset_button = tk.Button(root, 
                               text="New Game",
                               font=('Helvetica', 12),
                               bg='#27AE60',
                               fg='#ECF0F1',
                               activebackground='#219A52',
                               command=self.reset_game)
        reset_button.pack(pady=10)

    def button_click(self, row, col):
        index = 3 * row + col
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player,
                                     state=tk.DISABLED,
                                     disabledforeground='#E74C3C' if self.current_player == 'X' else '#3498DB')
            
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(text=f"Player {self.current_player}'s Turn")

    def check_winner(self):
        # Check rows, columns and diagonals
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        
        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == 
                self.board[combo[2]] != ""):
                # Highlight winning combination
                for i in combo:
                    self.buttons[i].config(bg='#27AE60')
                return True
        return False

    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        self.turn_label.config(text="Player X's Turn")
        for button in self.buttons:
            button.config(text="",
                        state=tk.NORMAL,
                        bg='#34495E')

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
