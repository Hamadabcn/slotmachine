import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
import os

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 10000

ROWS = 3
COLS = 3

IMAGE_FILENAMES = ["7.jpg", "watermelon.jpg", "cherries.jpg", "lemon.jpg", "orange.jpg"]
SYMBOLS = ["\u2665", "\u2666", "\u2663", "\u2660", "\u2728"]

symbol_count = {
    "\u2665": 5,
    "\u2666": 10,
    "\u2663": 15,
    "\u2660": 25,
    "\u2728": 2
}

symbol_value = {
    "\u2665": 100,
    "\u2666": 50,
    "\u2663": 25,
    "\u2660": 5,
    "\u2728": 2
}

FLASH_COLORS = ["#FF0000", "#FFFF00"]
FLASH_INTERVAL = 500

class InitialBalanceDialog(tk.Toplevel):
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
        self.label = tk.Label(self, text="How much do you want to bet:", font=("Arial", 20))
        self.entry = tk.Entry(self, font=("Arial", 12))
        self.ok_button = tk.Button(self, text="OK", command=self.ok_button_clicked, font=("Arial", 14), bg="#4CAF50",
                                fg="white")

        self.label.pack(pady=10)
        self.entry.pack(pady=5)
        self.ok_button.pack(pady=10)

    def ok_button_clicked(self):
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
    def __init__(self, initial_balance):
        self.balance = initial_balance

    def update_balance(self, result):
        self.balance += result

class SlotMachineLogic:
    @staticmethod
    def get_slot_machine_spin(rows, cols, symbols):
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
    def __init__(self, master, player):
        self.master = master
        self.master.title("Slot Machine Game")
        self.player = player

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 700) // 2
        master.geometry(f"+{x}+{y}")

        master.configure(bg="#FFFF00")

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

        self.symbol_images = []  # Store references to images at the class level
        self.original_symbol_images = []  # Store references to the original images at the class level

        for i in range(ROWS):
            row_frame = tk.Frame(self.master, bg="#FFFF00")
            row_frame.grid(row=5 + i, column=0, columnspan=COLS, pady=10, padx=10, sticky="w")

            row_images = []  # Store references to images for each row
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
                label.grid(row=0, column=j, padx=5, pady=5, sticky="nsew")
                row_frame.grid_columnconfigure(j, weight=1)  # Adjusted to make columns have a fixed width
                self.symbol_labels.append(label)
                row_images.append(None)  # Initialize with None

            self.original_symbol_images.append(row_images)

        self.result_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="n")
        self.balance_label.grid(row=1, column=0, columnspan=2, pady=10)
        self.lines_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.lines_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        self.bet_label.grid(row=3, column=0, pady=5, padx=10, sticky="e")
        self.bet_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        self.spin_button.grid(row=4, column=0, pady=20, padx=10, sticky="w")
        self.quit_button.grid(row=4, column=1, pady=20, padx=10, sticky="e")

    def quit_game(self):
        self.master.destroy()

    def spin(self):
        lines_str = self.lines_var.get()
        bet_str = self.bet_var.get()

        try:
            lines = int(lines_str)
            bet = int(bet_str)

            if 1 <= lines <= MAX_LINES and MIN_BET <= bet <= MAX_BET:
                if bet * lines <= self.player.balance:
                    self.player.balance -= bet * lines
                    self.balance_label.config(text=f"Balance: €{self.player.balance}")

                    columns = SlotMachineLogic.get_slot_machine_spin(ROWS, COLS, symbol_count)
                    winnings, winning_lines = SlotMachineLogic.check_winnings(columns, lines, bet, symbol_value)

                    if winnings > 0:
                        self.player.balance += winnings
                        self.balance_label.config(text=f"Balance: €{self.player.balance}")
                        self.result_var.set(f"Congratulations! You won €{winnings} on lines {', '.join(map(str, winning_lines))}.")
                    else:
                        self.result_var.set("Sorry, you didn't win anything. Try again!")

                    # Display symbols on the slot machine
                    for i in range(ROWS * COLS):
                        symbol = columns[i // ROWS][i % ROWS]
                        image_path = os.path.join(os.path.dirname(__file__), IMAGE_FILENAMES[SYMBOLS.index(symbol)])
                        image = Image.open(image_path)
                        image = image.resize((40, 40), resample=Image.BILINEAR)
                        photo = ImageTk.PhotoImage(image)
                        self.symbol_labels[i].configure(image=photo)
                        self.symbol_labels[i].image = photo
                        self.symbol_images.append(photo)
                else:
                    messagebox.showinfo("Insufficient Balance", "You don't have enough balance to place this bet. Please lower "
                                                                "your bet or number of lines.")
            else:
                messagebox.showinfo("Invalid Input", f"Lines must be between 1 and {MAX_LINES}, and bet must be between "
                                                    f"{MIN_BET} and {MAX_BET}.")
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter valid integers for lines and bet.")

    def display_result(self, result):
        self.result_var.set(result)

def main():
    root = tk.Tk()
    initial_balance_dialog = InitialBalanceDialog(root)
    root.wait_window(initial_balance_dialog)

    if hasattr(initial_balance_dialog, 'initial_balance'):
        player = Player(initial_balance_dialog.initial_balance)
        gui = SlotMachineGUI(root, player)
        root.mainloop()

if __name__ == "__main__":
    main()
