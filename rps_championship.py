#pyinstaller --onefile --windowed --icon=icon.ico rps_championship.py
import tkinter as tk
from tkinter import messagebox
import random
import sys
import os

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Championship")
        self.root.geometry("500x600")
        
        # Make window appear in the center of the screen
        self.center_window()
        
        # Initialize scores
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.max_rounds = 5
        
        # Create GUI elements
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        # Scoreboard frame
        score_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg='#f0f0f0')
        score_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(score_frame, text="ROCK PAPER SCISSORS CHAMPIONSHIP", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=5)
        
        self.score_label = tk.Label(score_frame, 
                                  text=f"You: {self.user_score}  |  Computer: {self.computer_score}  |  Round: {self.rounds_played}/{self.max_rounds}",
                                  font=('Arial', 12), bg='#f0f0f0')
        self.score_label.pack(pady=5)
        
        # Game title
        tk.Label(self.root, text="Make Your Choice:", font=('Arial', 16)).pack(pady=20)
        
        # Choice buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Choice buttons with better styling
        choices = ["Rock", "Paper", "Scissors"]
        button_colors = {
            "Rock": "#ff9999",
            "Paper": "#99ccff",
            "Scissors": "#99ff99"
        }
        
        for choice in choices:
            btn = tk.Button(button_frame, text=choice, width=10, height=2,
                           font=('Arial', 12, 'bold'), 
                           bg=button_colors[choice], activebackground=button_colors[choice],
                           command=lambda c=choice: self.play_round(c))
            btn.pack(side=tk.LEFT, padx=10, ipadx=5, ipady=5)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", font=('Arial', 14))
        self.result_label.pack(pady=20)
        
        # Computer choice display
        self.computer_choice_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.computer_choice_label.pack()
        
        # Reset button with better styling
        self.reset_btn = tk.Button(self.root, text="New Championship", state=tk.DISABLED,
                                 command=self.reset_game, font=('Arial', 12),
                                 bg='#ffcc99', activebackground='#ffcc99')
        self.reset_btn.pack(pady=20)
        
        # Exit button
        exit_btn = tk.Button(self.root, text="Exit Game", command=self.exit_game,
                           font=('Arial', 10), bg='#ff9999', activebackground='#ff9999')
        exit_btn.pack(side=tk.BOTTOM, pady=10)
    
    def play_round(self, user_choice):
        if self.rounds_played >= self.max_rounds:
            return
            
        # Computer makes random choice
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)
        
        # Display computer's choice
        self.computer_choice_label.config(text=f"Computer chose: {computer_choice}")
        
        # Determine winner
        result = self.determine_winner(user_choice, computer_choice)
        
        # Update scores and display result
        if "win" in result:
            self.user_score += 1
            color = "green"
        elif "lose" in result:
            self.computer_score += 1
            color = "red"
        else:
            color = "blue"
            
        self.result_label.config(text=result, fg=color)
        
        self.rounds_played += 1
        self.update_scoreboard()
        
        # Check if game is over
        if self.rounds_played >= self.max_rounds:
            self.end_game()
    
    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        
        win_conditions = {
            "Rock": "Scissors",
            "Paper": "Rock",
            "Scissors": "Paper"
        }
        
        if win_conditions[user_choice] == computer_choice:
            return f"You win this round! {user_choice} beats {computer_choice}"
        else:
            return f"You lose this round! {computer_choice} beats {user_choice}"
    
    def update_scoreboard(self):
        self.score_label.config(
            text=f"You: {self.user_score}  |  Computer: {self.computer_score}  |  Round: {self.rounds_played}/{self.max_rounds}"
        )
    
    def end_game(self):
        if self.user_score > self.computer_score:
            winner = "🏆 You won the championship! 🏆"
            color = "green"
        elif self.user_score < self.computer_score:
            winner = "💻 Computer won the championship! 💻"
            color = "red"
        else:
            winner = "🤝 The championship ended in a tie! 🤝"
            color = "blue"
        
        self.result_label.config(text=winner, fg=color)
        self.reset_btn.config(state=tk.NORMAL)
        
        # Show summary message
        messagebox.showinfo("Game Over", 
                          f"Final Score:\nYou: {self.user_score}\nComputer: {self.computer_score}\n\n{winner}")
    
    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        
        self.update_scoreboard()
        self.result_label.config(text="")
        self.computer_choice_label.config(text="")
        self.reset_btn.config(state=tk.DISABLED)
    
    def exit_game(self):
        self.root.destroy()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        icon_path = resource_path('icon.ico')
        root.iconbitmap(icon_path)
    except:
        pass  # Icon file not found
    
    game = RockPaperScissorsGame(root)
    root.mainloop()