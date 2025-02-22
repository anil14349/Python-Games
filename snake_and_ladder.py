import tkinter as tk
from tkinter import messagebox
import random

class SnakeAndLadder:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder")
        
        # Set minimum window size
        self.root.minsize(800, 600)
        
        # Define color scheme
        self.colors = {
            'bg': '#f0f2f5',  # Light gray-blue background
            'board_bg': '#ffffff',  # White board
            'text': '#2c3e50',  # Dark blue-gray text
            'accent': '#6c3483',  # Darker purple for new game
            'button': '#16a085',  # Dark teal for roll button
            'button_hover': '#117864',  # Even darker teal for hover
            'shadow': '#bdc3c7',  # Light gray
            'player1': '#e74c3c',  # Red
            'player2': '#9b59b6',  # Purple
            'snake': '#e74c3c',  # Red for snakes
            'ladder': '#f1c40f',  # Yellow for ladders
            'player1_light': '#fad4d1',  # Light red for player 1 cell
            'player2_light': '#e8d5f0',  # Light purple for player 2 cell
            'both_players': '#f5e6e9'  # Light pink when both players present
        }

        # Game state
        self.current_player = 1
        self.player1_pos = 1
        self.player2_pos = 1
        self.dice_value = 1
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        
        # Create dice images
        self.dice_images = self.create_dice_images()
        
        # Define snakes and ladders
        self.snakes = {
            16: 6,
            47: 26,
            49: 11,
            56: 53,
            62: 19,
            64: 60,
            87: 24,
            93: 73,
            95: 75,
            98: 78
        }
        
        self.ladders = {
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100
        }
        
        self.get_player_names()
        
    def create_dice_images(self):
        """Create dice face images using circles"""
        images = {}
        size = 80
        dot_size = 12
        
        for number in range(1, 7):
            # Create a PhotoImage for each dice face
            img = tk.PhotoImage(width=size, height=size)
            
            # Draw the white background and border
            for x in range(size):
                for y in range(size):
                    # Draw border
                    if x < 2 or x >= size-2 or y < 2 or y >= size-2:
                        img.put('#2c3e50', (x, y))  # Border color
                    else:
                        img.put('#ffffff', (x, y))  # White background
            
            # Define dot positions for each number
            dots = {
                1: [(size//2, size//2)],
                2: [(size//4, size//4), (3*size//4, 3*size//4)],
                3: [(size//4, size//4), (size//2, size//2), (3*size//4, 3*size//4)],
                4: [(size//4, size//4), (3*size//4, size//4), 
                    (size//4, 3*size//4), (3*size//4, 3*size//4)],
                5: [(size//4, size//4), (3*size//4, size//4),
                    (size//2, size//2),
                    (size//4, 3*size//4), (3*size//4, 3*size//4)],
                6: [(size//4, size//4), (3*size//4, size//4),
                    (size//4, size//2), (3*size//4, size//2),
                    (size//4, 3*size//4), (3*size//4, 3*size//4)]
            }
            
            # Draw dots for current number
            for cx, cy in dots[number]:
                # Draw a filled circle
                for x in range(cx-dot_size//2, cx+dot_size//2):
                    for y in range(cy-dot_size//2, cy+dot_size//2):
                        if (x-cx)**2 + (y-cy)**2 <= (dot_size//2)**2:
                            if 0 <= x < size and 0 <= y < size:
                                img.put('#2c3e50', (x, y))
            
            images[number] = img
        
        return images
    
    def get_player_names(self):
        """Show dialog to get player names"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Player Names")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("300x250")
        dialog.resizable(False, False)
        
        # Set dialog background
        dialog.configure(bg=self.colors['bg'])
        
        # Create and pack widgets
        frame = tk.Frame(dialog, padx=20, pady=20, bg=self.colors['bg'])
        frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            frame,
            text="Enter Player Names",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(pady=(0, 20))
        
        # Player 1 input
        p1_frame = tk.Frame(frame, bg=self.colors['bg'])
        p1_frame.pack(fill='x', pady=(0, 10))
        
        p1_label = tk.Label(
            p1_frame,
            text="Player 1:",
            font=('Helvetica', 12),
            bg=self.colors['bg'],
            fg=self.colors['player1'],
            width=10,
            anchor='w'
        )
        p1_label.pack(side='left')
        
        p1_entry = tk.Entry(
            p1_frame,
            font=('Helvetica', 12),
            bg='white',
            fg=self.colors['text'],
            insertbackground=self.colors['text'],  # Cursor color
            relief='solid',
            width=20
        )
        p1_entry.insert(0, "Player 1")
        p1_entry.pack(side='left', padx=5)
        
        # Player 2 input
        p2_frame = tk.Frame(frame, bg=self.colors['bg'])
        p2_frame.pack(fill='x', pady=(0, 20))
        
        p2_label = tk.Label(
            p2_frame,
            text="Player 2:",
            font=('Helvetica', 12),
            bg=self.colors['bg'],
            fg=self.colors['player2'],
            width=10,
            anchor='w'
        )
        p2_label.pack(side='left')
        
        p2_entry = tk.Entry(
            p2_frame,
            font=('Helvetica', 12),
            bg='white',
            fg=self.colors['text'],
            insertbackground=self.colors['text'],  # Cursor color
            relief='solid',
            width=20
        )
        p2_entry.insert(0, "Player 2")
        p2_entry.pack(side='left', padx=5)
        
        # Error label (hidden initially)
        error_label = tk.Label(
            frame,
            text="",
            font=('Helvetica', 10),
            bg=self.colors['bg'],
            fg='red'
        )
        error_label.pack()
        
        def validate_and_save():
            name1 = p1_entry.get().strip()
            name2 = p2_entry.get().strip()
            
            if not name1 or not name2:
                error_label.config(text="Please enter names for both players")
                return
            
            if name1 == name2:
                error_label.config(text="Players must have different names")
                return
            
            self.player1_name = name1
            self.player2_name = name2
            dialog.destroy()
            self.setup_gui()
        
        # Button frame
        button_frame = tk.Frame(frame, bg=self.colors['bg'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Start button
        start_button = tk.Button(
            button_frame,
            text="Start Game",
            command=validate_and_save,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['button'],
            fg='black',  # Changed to black
            activebackground=self.colors['button_hover'],
            activeforeground='black',  # Changed hover text to black
            relief='flat',
            cursor='hand2',
            width=15,
            height=2
        )
        start_button.pack()
        
        # Bind Enter key to validate_and_save
        dialog.bind('<Return>', lambda e: validate_and_save())
        
        # Select all text when entry gets focus
        def select_all(event):
            event.widget.select_range(0, 'end')
            return "break"
        
        p1_entry.bind('<FocusIn>', select_all)
        p2_entry.bind('<FocusIn>', select_all)
        
        # Set focus to first entry
        p1_entry.focus_set()
        
        # Center dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_gui(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'], padx=30, pady=20)
        self.main_container.pack(expand=True, fill='both')
        
        # Title
        title_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Snake & Ladder",
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title_label.pack(side='left')
        
        # Game area - create a container for board and right panel
        game_area = tk.Frame(self.main_container, bg=self.colors['bg'])
        game_area.pack(expand=True, fill='both')
        
        # Game board container with shadow effect (left side)
        board_container = tk.Frame(
            game_area,
            bg=self.colors['shadow'],
            padx=3,
            pady=3
        )
        board_container.pack(side='left', expand=True, fill='both', padx=(0, 20))
        
        # Game board
        self.board = tk.Frame(
            board_container,
            bg=self.colors['board_bg']
        )
        self.board.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Configure grid weights to ensure all rows are visible
        for i in range(10):
            self.board.grid_rowconfigure(i, weight=1, minsize=50)
            self.board.grid_columnconfigure(i, weight=1, minsize=50)
        
        # Create cells
        self.cells = {}
        numbers = list(range(100, 0, -1))
        
        for row in range(10):
            # Reverse numbers for alternate rows
            if row % 2 == 1:
                start = row * 10
                end = start + 10
                numbers[start:end] = reversed(numbers[start:end])
            
            for col in range(10):
                cell_num = numbers[row * 10 + col]
                
                # Cell frame
                cell = tk.Frame(
                    self.board,
                    bg=self.colors['board_bg'],
                    highlightthickness=1,
                    highlightbackground=self.colors['shadow']
                )
                cell.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
                
                # Configure cell grid weights
                cell.grid_rowconfigure(0, weight=1)
                cell.grid_columnconfigure(0, weight=1)
                
                # Inner frame for content
                inner_frame = tk.Frame(cell, bg=self.colors['board_bg'])
                inner_frame.grid(row=0, column=0)
                
                # Number label
                num_label = tk.Label(
                    inner_frame,
                    text=str(cell_num),
                    font=('Helvetica', 12, 'bold'),
                    bg=self.colors['board_bg'],
                    fg=self.colors['text'],
                    width=2
                )
                num_label.pack(pady=1)
                
                # Add snake/ladder indicators
                if cell_num in self.snakes:
                    tk.Label(
                        inner_frame,
                        text=f"↓{self.snakes[cell_num]}",
                        font=('Helvetica', 9),
                        fg=self.colors['snake'],
                        bg=self.colors['board_bg']
                    ).pack()
                elif cell_num in self.ladders:
                    tk.Label(
                        inner_frame,
                        text=f"↑{self.ladders[cell_num]}",
                        font=('Helvetica', 9),
                        fg=self.colors['ladder'],
                        bg=self.colors['board_bg']
                    ).pack()
                
                # Store references
                self.cells[cell_num] = {
                    'frame': cell,
                    'inner_frame': inner_frame,
                    'number': num_label
                }
        
        # Right side panel
        right_panel = tk.Frame(game_area, bg=self.colors['bg'], width=250)
        right_panel.pack(side='right', fill='y', padx=(0, 10))
        right_panel.pack_propagate(False)  # Maintain fixed width
        
        # Current Positions section
        positions_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        positions_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            positions_frame,
            text="Current Positions",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 10))
        
        # Player positions with colored backgrounds
        p1_pos_frame = tk.Frame(positions_frame, bg=self.colors['player1'], padx=15, pady=5)
        p1_pos_frame.pack(fill='x', pady=2)
        tk.Label(
            p1_pos_frame,
            text=f"{self.player1_name}:",
            font=('Helvetica', 12),
            fg='white',
            bg=self.colors['player1']
        ).pack(side='left')
        self.p1_pos_label = tk.Label(
            p1_pos_frame,
            text="1",
            font=('Helvetica', 12, 'bold'),
            fg='white',
            bg=self.colors['player1']
        )
        self.p1_pos_label.pack(side='right')
        
        p2_pos_frame = tk.Frame(positions_frame, bg=self.colors['player2'], padx=15, pady=5)
        p2_pos_frame.pack(fill='x', pady=2)
        tk.Label(
            p2_pos_frame,
            text=f"{self.player2_name}:",
            font=('Helvetica', 12),
            fg='white',
            bg=self.colors['player2']
        ).pack(side='left')
        self.p2_pos_label = tk.Label(
            p2_pos_frame,
            text="1",
            font=('Helvetica', 12, 'bold'),
            fg='white',
            bg=self.colors['player2']
        )
        self.p2_pos_label.pack(side='right')
        
        # Snakes & Ladders section
        legend_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        legend_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            legend_frame,
            text="Snakes & Ladders",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 10))
        
        # Snake indicator
        snake_frame = tk.Frame(legend_frame, bg=self.colors['bg'])
        snake_frame.pack(fill='x', pady=2)
        tk.Label(
            snake_frame,
            text="Snakes:",
            font=('Helvetica', 12),
            bg=self.colors['bg'],
            fg=self.colors['snake']
        ).pack(side='left')
        tk.Label(
            snake_frame,
            text="↓",
            font=('Helvetica', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['snake']
        ).pack(side='right')
        
        # Ladder indicator
        ladder_frame = tk.Frame(legend_frame, bg=self.colors['bg'])
        ladder_frame.pack(fill='x', pady=2)
        tk.Label(
            ladder_frame,
            text="Ladders:",
            font=('Helvetica', 12),
            bg=self.colors['bg'],
            fg=self.colors['ladder']
        ).pack(side='left')
        tk.Label(
            ladder_frame,
            text="↑",
            font=('Helvetica', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['ladder']
        ).pack(side='right')
        
        # Turn and controls section
        controls_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Turn indicator
        self.turn_label = tk.Label(
            controls_frame,
            text=f"{self.player1_name}'s Turn",
            font=('Helvetica', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['player1']
        )
        self.turn_label.pack(pady=(0, 15))
        
        # Roll button
        self.roll_button = tk.Button(
            controls_frame,
            text="Roll Dice",
            command=self.roll_dice,
            font=('Helvetica', 16, 'bold'),  # Bigger font
            bg=self.colors['button'],
            fg='black',  # Changed to black
            activebackground=self.colors['button_hover'],
            activeforeground='black',  # Changed hover text to black
            relief='flat',
            cursor='hand2',
            padx=30,  # More horizontal padding
            pady=12   # More vertical padding
        )
        self.roll_button.pack(pady=(0, 15))
        
        # Dice display
        self.dice_label = tk.Label(
            controls_frame,
            image=self.dice_images[1],
            bg=self.colors['board_bg'],
            relief='solid',
            borderwidth=1
        )
        self.dice_label.pack()
        
        # New Game button
        new_game_btn = tk.Button(
            right_panel,
            text="New Game",
            command=self.new_game,
            font=('Helvetica', 14, 'bold'),  # Bigger font
            bg=self.colors['accent'],
            fg='black',  # Changed to black
            activebackground=self.colors['button_hover'],
            activeforeground='black',  # Changed hover text to black
            relief='flat',
            cursor='hand2',
            padx=25,  # More horizontal padding
            pady=8    # More vertical padding
        )
        new_game_btn.pack(side='bottom', pady=20)
        
        # Initial board setup
        self.update_board()
        
    def update_board(self):
        # Reset all cell backgrounds
        for cell in self.cells.values():
            cell['frame'].configure(bg=self.colors['board_bg'])
            cell['inner_frame'].configure(bg=self.colors['board_bg'])
            cell['number'].configure(bg=self.colors['board_bg'])
            
            # Update snake/ladder indicators background
            for widget in cell['inner_frame'].winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=self.colors['board_bg'])
        
        # Update cell colors based on player positions
        if self.player1_pos > 0 and self.player2_pos > 0 and self.player1_pos == self.player2_pos:
            # Both players on same cell
            cell = self.cells[self.player1_pos]
            new_bg = self.colors['both_players']
            cell['frame'].configure(bg=new_bg)
            cell['inner_frame'].configure(bg=new_bg)
            cell['number'].configure(bg=new_bg)
            # Update snake/ladder indicators background
            for widget in cell['inner_frame'].winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=new_bg)
        else:
            # Players on different cells
            if self.player1_pos > 0:
                cell = self.cells[self.player1_pos]
                new_bg = self.colors['player1_light']
                cell['frame'].configure(bg=new_bg)
                cell['inner_frame'].configure(bg=new_bg)
                cell['number'].configure(bg=new_bg)
                # Update snake/ladder indicators background
                for widget in cell['inner_frame'].winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=new_bg)
            
            if self.player2_pos > 0:
                cell = self.cells[self.player2_pos]
                new_bg = self.colors['player2_light']
                cell['frame'].configure(bg=new_bg)
                cell['inner_frame'].configure(bg=new_bg)
                cell['number'].configure(bg=new_bg)
                # Update snake/ladder indicators background
                for widget in cell['inner_frame'].winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=new_bg)
    
    def roll_dice(self):
        self.dice_value = random.randint(1, 6)
        self.dice_label.configure(image=self.dice_images[self.dice_value])
        
        # Move player with animation
        if self.current_player == 1:
            old_pos = self.player1_pos
            new_pos = min(100, self.player1_pos + self.dice_value)
            
            # Check for snake or ladder
            if new_pos in self.snakes:
                new_pos = self.snakes[new_pos]
                messagebox.showinfo("Oops!", f"{self.player1_name} hit a snake! Go down to {new_pos}")
            elif new_pos in self.ladders:
                new_pos = self.ladders[new_pos]
                messagebox.showinfo("Yay!", f"{self.player1_name} found a ladder! Go up to {new_pos}")
            
            self.player1_pos = new_pos
            
        else:
            old_pos = self.player2_pos
            new_pos = min(100, self.player2_pos + self.dice_value)
            
            # Check for snake or ladder
            if new_pos in self.snakes:
                new_pos = self.snakes[new_pos]
                messagebox.showinfo("Oops!", f"{self.player2_name} hit a snake! Go down to {new_pos}")
            elif new_pos in self.ladders:
                new_pos = self.ladders[new_pos]
                messagebox.showinfo("Yay!", f"{self.player2_name} found a ladder! Go up to {new_pos}")
            
            self.player2_pos = new_pos
        
        # Update position labels
        self.p1_pos_label.config(text=str(self.player1_pos))
        self.p2_pos_label.config(text=str(self.player2_pos))
        
        # Update board
        self.update_board()
        
        # Check for win with enhanced message
        if self.player1_pos == 100:
            messagebox.showinfo(" Congratulations! ", f"{self.player1_name} wins the game! ")
            self.new_game()
            return
        elif self.player2_pos == 100:
            messagebox.showinfo(" Congratulations! ", f"{self.player2_name} wins the game! ")
            self.new_game()
            return
        
        # Switch player with enhanced display
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
        current_name = self.player1_name if self.current_player == 1 else self.player2_name
        player_color = self.colors['player1'] if self.current_player == 1 else self.colors['player2']
        self.turn_label.configure(
            text=f"{current_name}'s Turn ",
            fg=player_color
        )
    
    def new_game(self):
        self.current_player = 1
        self.player1_pos = 1
        self.player2_pos = 1
        self.dice_value = 1
        self.dice_label.configure(image=self.dice_images[1])
        self.turn_label.configure(text=f"{self.player1_name}'s Turn", fg=self.colors['player1'])
        self.update_board()
        # Reset position labels
        self.p1_pos_label.config(text="1")
        self.p2_pos_label.config(text="1")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadder(root)
    root.mainloop()
