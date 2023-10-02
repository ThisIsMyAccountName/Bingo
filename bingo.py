import random
import os
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Bingo Game")

cell_size = 60
board_size = 90

numbers = []
missing_numbers = []
bingo_board = []
file_path = 'bingo_game_state.txt'  # Specify the file name to look for in the program's directory

def find_missing_numbers(numbers):  
    global missing_numbers
    missing_numbers = [i for i in range(1, board_size + 1) if i not in numbers]


def generate_bingo_board1(max_num):
    board = [[' ' for _ in range(5)] for _ in range(5)]
    max_num = int(max_num / 5)
    columns = [random.sample(range(1, int(max_num)*1+1), 5),
                random.sample(range(int(max_num)*1+1, int(max_num)*2+1), 5),
                random.sample(range(int(max_num)*2+1, int(max_num)*3+1), 5),
                random.sample(range(int(max_num)*3+1, int(max_num)*4+1), 5),
                random.sample(range(int(max_num)*4+1, int(max_num)*5+1), 5)]
    
    for col_idx in range(5):
        for row_idx in range(5):
            number = columns[col_idx][row_idx]
            board[row_idx][col_idx] = str(number)

    return board

def generate_bingo_board(max_num):
    numbers = random.sample(range(1, max_num + 1), 25)
    return [numbers[i:i+5] for i in range(0, 25, 5)]


def on_number_entry(event = None, numb = -1):
    number = number_entry.get()
    if (x:=number.isdigit()) or numb >= 0:
        number = int(number) if x else numb
        if 1 <= number <= board_size and number not in numbers:
            numbers.append(number)
            update_gui()
            error_message_var.set("")
        else:
            error_message_var.set(f"Please enter a valid number between 1 and {board_size}.")
    else:
        error_message_var.set("Please enter a valid number.")
    
    number_entry.delete(0, tk.END)
    
def on_delete_entry(event = None, numb = -1):
    number = number_entry.get()
    if (x:=number.isdigit()) or numb >= 0:
        number = number = int(number) if x else numb
        if number in numbers:
            numbers.remove(number)
            update_gui()
            number_entry.delete(0, tk.END) 
            error_message_var.set("") 
        else:
            error_message_var.set(f"Number {number} is not in the list.")
    else:
        error_message_var.set("Please enter a valid number.")

def update_bingo_board():
    for row_idx, row in enumerate(bingo_board):
        for col_idx, cell_value in enumerate(row):
            if int(cell_value) in numbers:
                cell_entry = bingo_cells[row_idx][col_idx]
                drawCanv.itemconfig(cell_entry[0], fill="green")
                drawCanv.itemconfig(cell_entry[1], fill="black", text=cell_value)
            else:
                cell_entry = bingo_cells[row_idx][col_idx]
                drawCanv.itemconfig(cell_entry[0], fill="white")
                drawCanv.itemconfig(cell_entry[1], fill="black", text=cell_value)

def find_clicked_cell(event):
    x, y = event.x, event.y
    for row_idx, row in enumerate(bingo_cells):
        for col_idx, cell_entry in enumerate(row):
            x1, y1, x2, y2 = drawCanv.coords(cell_entry[0])
            if x1 <= x <= x2 and y1 <= y <= y2:
                numb = int(bingo_board[row_idx][col_idx])
                if numb in numbers:
                    on_delete_entry(numb=numb)
                else:
                    on_number_entry(numb=numb)
            
def create_bingo_canvas(canvas, CELL_SIZE=60):
    bingo_cells = []

    for row_idx in range(5):
        cell_entries = []
        for col_idx in range(5):
            x1 = col_idx * CELL_SIZE
            y1 = row_idx * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            rectangle = canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white", )
            text = canvas.create_text(x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2, text="", font=("Arial", 20))
            cell_entries.append((rectangle, text))
            canvas.tag_bind(rectangle, '<Button-1>', find_clicked_cell) 
            canvas.tag_bind(text, '<Button-1>', find_clicked_cell)
        bingo_cells.append(cell_entries)

    return bingo_cells

def check_if_bingo(privious_bingos):
    for row in bingo_board:
        if all([int(cell) in numbers for cell in row]):
            return True
        for col_idx in range(5):
            if all([int(bingo_board[row_idx][col_idx]) in numbers for row_idx in range(5)]):
                return True
    if all([int(bingo_board[i][i]) in numbers for i in range(5)]):
        return True
    if all([int(bingo_board[i][4-i]) in numbers for i in range(5)]):
        return True
    return False

def create_numbers_canvas(canvas, numbers):
    for i, number in enumerate(numbers, start=1):
        row = (i - 1) // 5  
        col = (i - 1) % 5   
        x = 20 + col * 30   
        y = 40 + row * 20   
        canvas.create_text(x, y, text=str(number), font=("Arial", 12))

def update_numbers_sections(missing_numbers):
    missing_numbers_canvas.delete("all")
    taken_numbers_canvas.delete("all")

    # Display missing numbers on the left
    missing_numbers_canvas.create_text(60, 20, text="Missing Numbers", font=("Arial", 12))
    create_numbers_canvas(missing_numbers_canvas, missing_numbers)

    # Display taken numbers on the right
    taken_numbers_canvas.create_text(60, 20, text="Taken Numbers", font=("Arial", 12))
    create_numbers_canvas(taken_numbers_canvas, numbers)

if os.path.exists(file_path):
    file_path = 'bingo_game_state.txt'  # Specify the file name to look for in the program's directory
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                numbers = [int(line.strip()) for line in lines[0].strip().split(',')]
                missing_numbers = [int(line.strip()) for line in lines[1].strip().split(',')]
                bingo_board = [line.strip().split(',') for line in lines[2:]]
else:
    bingo_board = generate_bingo_board(board_size)

def reset_game():
    global numbers, missing_numbers, bingo_board
    confirmation = messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset the game?", default=messagebox.NO)
    if confirmation:
        numbers = []
        missing_numbers = []
        
        bingo_board = generate_bingo_board(board_size)
        update_gui()
        
        if os.path.exists(file_path):
            os.remove(file_path)
    

# Function to save numbers, taken_numbers, and bingo_board to a file
def save_game_state_to_file():
    if numbers:
        file_path = 'bingo_game_state.txt'  # Specify the file name to save in the program's directory
        with open(file_path, 'w') as file:
            file.write(','.join(map(str, numbers)) + '\n')
            file.write(','.join(map(str, missing_numbers)) + '\n')
            for row in bingo_board:
                file.write(','.join(map(str, row)) + '\n')

def update_gui():
    find_missing_numbers(numbers)
    update_numbers_sections(missing_numbers)
    save_game_state_to_file()
    update_bingo_board()


# Create the canvas for the bingo board
drawCanv = tk.Canvas(root, width=300, height=300, bd=0)
drawCanv.grid(row=0, column=5, rowspan=7, padx=10, pady=10)
bingo_cells = create_bingo_canvas(drawCanv, cell_size)

number_entry_label = tk.Label(root, text="Enter a number:")
number_entry_label.grid(row=7, column=2, columnspan=5)

number_entry = tk.Entry(root)
number_entry.grid(row=8, column=2, columnspan=5)
number_entry.focus()

button_frame = tk.Frame(root)
button_frame.grid(row=9, column=2, columnspan=5)

submit_button = tk.Button(button_frame, text="Submit", command=on_number_entry)
submit_button.grid(row=0, column=2, padx=5)

delete_button = tk.Button(button_frame, text="Delete", command=on_delete_entry)
delete_button.grid(row=0, column=6, padx=5)

reset_button = tk.Button(root, text="Reset Game", command=reset_game, font=("Helvetica", 20))
reset_button.grid(row=12, column=7, padx=10, pady=10)

error_message_var = tk.StringVar()
error_message_label = tk.Label(root, textvariable=error_message_var, fg="red")
error_message_label.grid(row=11, column=2, columnspan=5)

number_entry.bind('<Return>', on_number_entry)

missing_numbers_canvas = tk.Canvas(root, width=150, height=400, bd=0)
missing_numbers_canvas.grid(row=0, column=0, rowspan=12, padx=10, pady=1)

taken_numbers_canvas = tk.Canvas(root, width=150, height=400, bd=0)
taken_numbers_canvas.grid(row=0, column=7, rowspan=12, padx=10, pady=1)

update_gui()


root.mainloop()
