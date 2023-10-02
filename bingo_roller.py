import random
import tkinter as tk
import os
from tkinter import messagebox

board_size = 90
numbers = list(range(1, board_size + 1))
taken_numbers = []
undone_numbers = []

# Change the file path to name of the game or some way to identify the save file
save_file = 'bingo_save.txt'
if os.path.exists(save_file):
    with open(save_file, 'r') as file:
        saved_state = file.readlines()
        if len(saved_state) == 2:
            numbers = list(map(int, saved_state[0].strip().split(',')))
            taken_numbers = list(map(int, saved_state[1].strip().split(',')))

def generate_random_number():
    if numbers:
        if undone_numbers:
            number = undone_numbers.pop()
        else:
            number = random.choice(numbers)
            numbers.remove(number)

        taken_numbers.append(number)

        current_number_label.config(text=str(number))
        remaining_numbers = list(set(numbers) | set(undone_numbers))
        update_numbers_sections(remaining_numbers, taken_numbers)

        # Save the game state after each number is generated
        save_game_state()

    else:
        current_number_label.config(text="No\n More\n Numbers", font=("Helvetica", 40))

def save_game_state():
    # Save the current game state to a text file
    with open(save_file, 'w') as file:
        file.write(','.join(map(str, numbers)) + '\n')
        file.write(','.join(map(str, taken_numbers)))

def undo_last_number():
    if taken_numbers:
        number = taken_numbers.pop()
        undone_numbers.append(number)
        current_number_label.config(text=str(taken_numbers[-1]))
        remaining_numbers = list(set(numbers) | set(undone_numbers))
        update_numbers_sections(remaining_numbers, taken_numbers)

        # Save the game state after undoing the last number
        save_game_state()

def reset_game():
    global numbers, taken_numbers, undone_numbers
    # Ask for confirmation before resetting the game with the default button set to "No"
    confirmation = messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset the game?", default=messagebox.NO)
    
    if confirmation:
        numbers = list(range(1, board_size + 1))
        taken_numbers = []
        undone_numbers = []

        # Delete the save file if it exists
        if os.path.exists(save_file):
            os.remove(save_file)

        # Reset the display
        current_number_label.config(text="0")
        update_numbers_sections(numbers, taken_numbers)

def create_numbers_canvas(canvas, numbers, color):
    for i, number in enumerate(range(1, board_size+1), start=1):
        row = (i - 1) // 5
        col = (i - 1) % 5
        x = 30 + col * 40
        y = 50 + row * 30
        if number not in numbers:
            canvas.create_text(x, y, text=str(number), fill=color, font=("Arial", 25))
        else:
            canvas.create_text(x, y, text=str(number), font=("Arial", 25))

def update_numbers_sections(missing_numbers, taken_numbers):
    missing_numbers_canvas.delete("all")
    taken_numbers_canvas.delete("all")

    missing_numbers_canvas.create_text(120, 20, text="Missing Numbers", font=("Arial", 30))
    create_numbers_canvas(missing_numbers_canvas, missing_numbers, "gray")

    taken_numbers_canvas.create_text(120, 20, text="Taken Numbers", font=("Arial", 30))
    for i, number in enumerate(taken_numbers, start=1):
        row = (i - 1) // 5
        col = (i - 1) % 5
        x = 30 + col * 40
        y = 50 + row * 30
        taken_numbers_canvas.create_text(x, y, text=str(number), font=("Arial", 25))

root = tk.Tk()
root.title("Bingo Roller")

current_number_label = tk.Label(root, text="", font=("Helvetica", 200))
current_number_label.grid(row=0, column=1)

generate_button = tk.Button(root, text="Next Number", command=generate_random_number, font=("Helvetica", 30))
generate_button.grid(row=1, column=1)

undo_button = tk.Button(root, text="Undo", command=undo_last_number, font=("Helvetica", 20))
undo_button.grid(row=2, column=0)

reset_button = tk.Button(root, text="Reset Game", command=reset_game, font=("Helvetica", 20))
reset_button.grid(row=2, column=1)

root.bind('<Return>', lambda event=None: generate_random_number())
root.bind('<BackSpace>', lambda event=None: undo_last_number())

missing_numbers_canvas = tk.Canvas(root, width=300, height=600, bd=0)
missing_numbers_canvas.grid(row=0, column=0, rowspan=12, padx=10, pady=10)

taken_numbers_canvas = tk.Canvas(root, width=300, height=600, bd=0)
taken_numbers_canvas.grid(row=0, column=2, rowspan=12, padx=10, pady=10)

# Display the initial game state
update_numbers_sections(numbers, taken_numbers)

# Display the last taken number or "0" if there are no taken numbers
if taken_numbers:
    current_number_label.config(text=str(taken_numbers[-1]))
else:
    current_number_label.config(text="0")

root.mainloop()
