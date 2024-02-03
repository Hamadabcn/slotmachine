import pygame
import random
import sys

MAX_LINES = 3
MAX_BET = 10000
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 500,
    "B": 600,
    "C": 700,
    "D": 800,
    "F": 2000
}
symbol_value = {
    "A": 10000,
    "B": 2500,
    "C": 500,
    "D": 100,
    "F": 50
}

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slot Machine")

# Set up fonts
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 48)  # Add this line

def draw_text(lines, x, y, font, color=(255, 255, 255)):
    for i, text in enumerate(lines):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y + i * font.get_height()))

def draw_result(result):
    y = 60
    for line in result:
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (10, y))
        y += font.get_height() + 5

def draw_slot_machine(columns):  # Add the missing draw_slot_machine function
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            symbol_text = font.render(column[row], True, (255, 255, 255))
            screen.blit(symbol_text, (i * (WIDTH // COLS), row * (HEIGHT // ROWS)))

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
            value = random.choice(current_symbol)
            current_symbol.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def deposit():
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.isdigit():
                    return int(input_text)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                    input_text += event.unicode

        screen.fill((0, 0, 0))  # Clear the screen
        draw_text(["Enter deposit amount (Press Enter to submit):", input_text], 10, 10, font)
        pygame.display.flip()

def get_number_of_lines():
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.isdigit():
                    return int(input_text)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                    input_text += event.unicode

        screen.fill((0, 0, 0))  # Clear the screen
        draw_text(["Enter the number of lines to bet on (1-3, Press Enter to submit):", input_text], 10, 10, font)
        pygame.display.flip()

def get_bet():
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.isdigit():
                    return int(input_text)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                    input_text += event.unicode

        screen.fill((0, 0, 0))  # Clear the screen
        draw_text([f"Enter the bet amount (€{MIN_BET} - €{MAX_BET}, Press Enter to submit):", input_text], 10, 10, font)
        pygame.display.flip()

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            result_text = [f"You do not have enough money to bet that amount, your current balance is: €{balance}"]
            draw_text(result_text, 10, 60, big_font)
            pygame.display.flip()
            pygame.time.delay(2000)  # Display the message for 2 seconds
            return result_text, 0
        else:
            break

    result_text = [f"You are betting €{bet} on {lines} lines. Total bet is equal to: €{total_bet}"]

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    draw_slot_machine(slots)
    pygame.display.flip()

    pygame.time.delay(1000)  # Display the result for 1 second

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    if winnings > 0:
        result_text.append(f"You won: €{winnings}")
        result_text.append(f"You won on lines: {', '.join(map(str, winning_lines))}")

    draw_result(result_text)  # Draw the result directly on the window

    pygame.display.flip()

    return result_text, winnings - total_bet


def draw_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            symbol_text = font.render(column[row], True, (255, 255, 255))
            screen.blit(symbol_text, (i * (WIDTH // COLS), row * (HEIGHT // ROWS)))

def main():
    balance = deposit()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"You left with €{balance}")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result, balance_change = spin(balance)
                    balance += balance_change
                elif event.key == pygame.K_q:
                    print(f"You left with €{balance}")
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))  # Clear the screen

        draw_text([f"Your Balance: €{balance}"], 10, 10, font)
        pygame.display.flip()

        clock.tick(60)  # Limit the frame rate to 60 FPS

if __name__ == "__main__":
    main()
