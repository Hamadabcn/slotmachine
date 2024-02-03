# a gambling slot machine in python and tKinter

import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time
import pygame
from pathlib import Path

# Constants
MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100000

ROWS = 3
COLS = 3

# Symbol definitions with counts and values
# Decreased symbol count for a lower winning probability
symbol_count = {
    "\u2665": 5,    # Heart symbol
    "\u2666": 10,   # Diamond symbol
    "\u2663": 15,   # Club symbol
    "\u2660": 25,   # Spade symbol
    "\u2728": 2     # Sparkle/star symbol
}

# Decreased symbol values for a lower winning probability
symbol_value = {
    "\u2665": 100,  # Heart symbol
    "\u2666": 50,   # Diamond symbol
    "\u2663": 25,   # Club symbol
    "\u2660": 5,    # Spade symbol
    "\u2728": 2     # Sparkle/star symbol
}

# Constants for Flash Colors and Flash Interval
FLASH_COLORS = ["#FF0000", "#FFFF00"]
FLASH_INTERVAL = 500

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Load the sound file
spin_sound = pygame.mixer.Sound("slotmachine.mp3")  # Replace with your sound file

class InitialBalanceDialog(tk.Toplevel):
    """Dialog to get the initial balance from the user."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Initial Balance")
        self.geometry("400x150")

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        self.geometry(f"+{x}+{y}")

        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the initial balance dialog."""
        self.label = tk.Label(self, text="How much do you want to bet:", font=("Arial", 20))
        self.entry = tk.Entry(self, font=("Arial", 12))
        self.ok_button = tk.Button(self, text="OK", command=self.ok_button_clicked, font=("Arial", 14), bg="#4CAF50",
                                fg="white")

        self.label.pack(pady=10)
        self.entry.pack(pady=5)
        self.ok_button.pack(pady=10)

    def ok_button_clicked(self):
        """Handle OK button click event."""
        try:
            initial_balance = int(self.entry.get())
            if initial_balance >= 0:
                self.initial_balance = initial_balance
                self.destroy()
            else:
                messagebox.showinfo("Invalid Input", "Initial balance must be a non-negative integer.")
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter a valid integer.")
        except tk.TclError:
            messagebox.showinfo("Canceled", "Initial balance input canceled.")

class Player:
    """Class representing the player with a balance."""
    
    def __init__(self, initial_balance):
        """Initialize the player with an initial balance."""
        self.balance = initial_balance

    def update_balance(self, result):
        """Update the player's balance."""
        self.balance += result

class SlotMachineLogic:
    """Class containing the logic for the slot machine."""
    
    @staticmethod
    def get_slot_machine_spin(rows, cols, symbols):
        """
        Generate a random slot machine spin.

        Parameters:
        - rows (int): Number of rows in the slot machine.
        - cols (int): Number of columns in the slot machine.
        - symbols (dict): Dictionary containing symbol counts.

        Returns:
        - list: 2D list representing the slot machine spin.
        """
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)

        columns = []
        for _ in range(cols):
            column = []
            current_symbol = all_symbols[:]
            for _ in range(rows):
                column.append(random.choice(current_symbol))
            columns.append(column)

        return columns

    @staticmethod
    def check_winnings(columns, lines, bet, values):
        """
        Check for winnings in the slot machine spin.

        Parameters:
        - columns (list): 2D list representing the slot machine spin.
        - lines (int): Number of lines to check for winnings.
        - bet (int): Bet amount per line.
        - values (dict): Dictionary containing symbol values.

        Returns:
        - tuple: A tuple containing the total winnings and a list of winning lines.
        """
        winnings = 0
        winning_lines = []

        for line in range(lines):
            symbol = columns[line][0]
            for symbol_to_check in columns[line]:
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

class SlotMachineGUI:
    """Class representing the graphical user interface for the slot machine game."""
    
    def __init__(self, master, player):
        """
        Initialize the slot machine GUI.

        Parameters:
        - master: The master widget (usually the Tk root window).
        - player (Player): An instance of the Player class.
        """
        self.master = master
        self.master.title("Slot Machine Game")
        self.player = player

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 700) // 2
        master.geometry(f"+{x}+{y}")

        master.configure(bg="#FFFF00")

        self.create_widgets()
        
        # Load the winning sound file
        sound_file_path = Path(__file__).parent / "won.mp3"
        self.winning_sound = pygame.mixer.Sound(str(sound_file_path))

    def create_widgets(self):
        """Create widgets for the slot machine GUI."""
        self.result_var = tk.StringVar()
        self.result_label = tk.Label(self.master, textvariable=self.result_var, font=("Arial", 16), bg="#4CAF50",
                                    fg="white", padx=10, pady=10)

        self.balance_label = tk.Label(self.master, text=f"Balance: €{self.player.balance}", font=("Arial", 14),
                                    bg="#FFFF00")
        self.lines_label = tk.Label(self.master, text="Number of Lines:", font=("Arial", 14),
                                    bg="#FFFF00")
        self.bet_label = tk.Label(self.master, text="Bet per Line:", font=("Arial", 14),
                                bg="#FFFF00")

        self.lines_var = tk.StringVar()
        self.lines_entry = tk.Entry(self.master, textvariable=self.lines_var, font=("Arial", 14))

        self.bet_var = tk.StringVar()
        self.bet_entry = tk.Entry(self.master, textvariable=self.bet_var, font=("Arial", 14))

        self.symbol_labels = []

        self.spin_button = tk.Button(self.master, text="Spin", command=self.spin, font=("Arial", 14), bg="#2196F3",
                                    fg="white", padx=20, pady=10)
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game, font=("Arial", 14), bg="#D9534F",
                                    fg="white", padx=20, pady=10)

        for i in range(ROWS):
            row_frame = tk.Frame(self.master, bg="#FFFF00")
            row_frame.grid(row=5 + i, column=0, columnspan=COLS, pady=10, padx=10, sticky="w")

            for j in range(COLS):
                label = tk.Label(
                    row_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=4,
                    height=2,
                    relief="ridge",
                    bg="#FFFF00",
                    anchor="center",
                    padx=2,
                    pady=2
                )
                label.grid(row=0, column=j, padx=5, pady=5)
                row_frame.grid_columnconfigure(j, minsize=40)
                self.symbol_labels.append(label)

        self.result_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="n")
        self.balance_label.grid(row=1, column=0, columnspan=2, pady=10)
        self.lines_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.lines_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        self.bet_label.grid(row=3, column=0, pady=5, padx=10, sticky="e")
        self.bet_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        self.spin_button.grid(row=4, column=0, pady=20, padx=(0, 10), sticky="e")  # Added padx=(0, 10) for separation
        self.quit_button.grid(row=4, column=1, pady=20, padx=(10, 0), sticky="w")  # Added padx=(10, 0) for separation

    def spin(self):
        """Handle the spin button click event."""
        lines = self.lines_var.get()
        bet = self.bet_var.get()

        try:
            lines = int(lines)
            bet = int(bet)

            if lines <= 0 or bet <= 0:
                raise ValueError("Lines and bet must be positive integers.")

            if 1 <= lines <= MAX_LINES and MIN_BET <= bet <= MAX_BET:
                total_bet = bet * lines

                if total_bet > self.player.balance:
                    messagebox.showinfo("Insufficient Balance",
                                        f"You do not have enough money to bet that amount. Your current balance is: €{self.player.balance}")
                else:
                    # Perform the spin with the spinning effect
                    self.spin_with_effect(lines, bet)
            else:
                messagebox.showinfo("Invalid Input", "Please enter valid values for lines and bet.")
        except ValueError as e:
            messagebox.showinfo("Invalid Input", str(e))

    def spin_with_effect(self, lines, bet):
        spin_duration = 2

        # Play the spin sound
        spin_sound.play()

        start_time = time.time()

        while time.time() - start_time < spin_duration:
            slots = SlotMachineLogic.get_slot_machine_spin(ROWS, COLS, symbol_count)
            self.display_slot_machine(slots)
            self.master.update()
            time.sleep(0.1)

        # Stop the spin sound
        spin_sound.stop()

        result = self.perform_spin(lines, bet)
        self.update_balance(result)

    def perform_spin(self, lines, bet):
        """
        Perform a slot machine spin.

        Parameters:
        - lines (int): Number of lines to bet on.
        - bet (int): Bet amount per line.

        Returns:
        - int: The result of the spin.
        """
        try:
            slots = SlotMachineLogic.get_slot_machine_spin(ROWS, COLS, symbol_count)
            self.display_slot_machine(slots)
            winnings, winning_lines = SlotMachineLogic.check_winnings(slots, lines, bet, symbol_value)
            result_text = f"You won: €{winnings}\n"
            result_text += f"You won on line: {winning_lines}"
            self.result_var.set(result_text)

            if winnings > 0:
                self.flash_background()
                self.play_winning_sound()  # Play the winning sound

            return winnings - (bet * lines)
        except ValueError as e:
            messagebox.showinfo("Invalid Input", str(e))
            return 0
        except tk.TclError:
            messagebox.showinfo("Error", "An unexpected error occurred.")
            return 0
        
    def play_winning_sound(self):
        # Play the winning sound
        self.winning_sound.play()

    def flash_background(self):
        """Flash the background of the GUI."""
        self.master.after_cancel(self.flash_background)
        self.flash_index = 0
        self.flash_background_helper()

    def flash_background_helper(self):
        """Helper function for flashing the background."""
        if self.flash_index < len(FLASH_COLORS):
            color = FLASH_COLORS[self.flash_index]
            self.master.configure(bg=color)
            self.flash_index += 1
            self.master.after(FLASH_INTERVAL, self.flash_background_helper)
        else:
            self.master.configure(bg="#FFFF00")

    def display_slot_machine(self, columns):
        """
        Display the slot machine spin on the GUI.

        Parameters:
        - columns (list): 2D list representing the slot machine spin.
        """
        for i, column in enumerate(columns):
            for j, symbol in enumerate(column):
                self.symbol_labels[i * COLS + j].config(text=symbol)

    def update_balance(self, result):
        """
        Update the player's balance and the GUI.

        Parameters:
        - result (int): Result of the slot machine spin.
        """
        self.player.update_balance(result)
        self.balance_label.config(text=f"Balance: €{self.player.balance}")

    def quit_game(self):
        """Handle quitting the game."""
        self.master.destroy()

def main():
    """Main function to run the slot machine game."""
    root = tk.Tk()
    initial_balance_dialog = InitialBalanceDialog(root)
    root.wait_window(initial_balance_dialog)
    initial_balance = getattr(initial_balance_dialog, 'initial_balance', 0)
    player = Player(initial_balance)
    gui = SlotMachineGUI(root, player)
    root.mainloop()

if __name__ == "__main__":
    main()
