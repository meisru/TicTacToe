import tkinter as tk
import random
from tkinter import messagebox

lightPink = "#ffdbdb"
darkPink = "#ffc6c6"
brown = "#644a07"

root = tk.Tk()
root.title("Tic Tac Toe")
root.resizable(0, 0)
root.configure(bg=lightPink)

try:
    humanImg = tk.PhotoImage(file="assets/human.png").subsample(20, 20)
    computerImg = tk.PhotoImage(file="assets/computer.png").subsample(20, 20)
except tk.TclError:
    messagebox.showerror("Error", "Image files not found.")
    root.destroy()

buttons = [[None for _ in range(3)] for _ in range(3)]
buttons_content = [[0 for _ in range(3)] for _ in range(3)]

game = None  # Will hold the current game object

def possibilities():
    return [[i, j] for i in range(3) for j in range(3) if buttons_content[i][j] == 0]

def random_position(letter):
    if possibilities():
        row, col = random.choice(possibilities())
        buttons_content[row][col] = letter
        buttons[row][col].config(text=letter, state="disabled")
        return True
    return False

def position_availability(row, col, letter):
    if buttons_content[row][col] == 0:
        buttons_content[row][col] = letter
        buttons[row][col].config(text=letter, state="disabled")
        return True
    return False

def win(letter):
    for r in range(3):
        if all(buttons_content[r][c] == letter for c in range(3)):
            return True
    for c in range(3):
        if all(buttons_content[r][c] == letter for r in range(3)):
            return True
    if all(buttons_content[i][i] == letter for i in range(3)):
        return True
    if all(buttons_content[i][2 - i] == letter for i in range(3)):
        return True
    return False

def draw():
    return all(buttons_content[i][j] != 0 for i in range(3) for j in range(3))

class Player:
    def __init__(self, letter):
        self.letter = letter

class ComputerPlayer(Player):
    def move(self):
        opponent = "o" if self.letter == "x" else "x"

        for i, j in possibilities():
            buttons_content[i][j] = self.letter
            if win(self.letter):
                buttons[i][j].config(text=self.letter, state="disabled")
                return
            buttons_content[i][j] = 0

        for i, j in possibilities():
            buttons_content[i][j] = opponent
            if win(opponent):
                buttons_content[i][j] = self.letter
                buttons[i][j].config(text=self.letter, state="disabled")
                return
            buttons_content[i][j] = 0

        random_position(self.letter)

class HumanPlayer(Player):
    def move(self, row, col):
        if position_availability(row, col, self.letter):
            return True
        else:
            mainLabel.config(text="Position already taken!")
            return False


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.turn = self.p1

    def handle_click(self, row, col):
        if isinstance(self.turn, HumanPlayer):
            if self.turn.move(row, col):
                if win(self.turn.letter):
                    messagebox.showinfo("Game Over", f"{self.turn.letter} wins!")
                    self.disable_board()
                    self.play_again()
                elif draw():
                    mainLabel.config(text="It's a draw!")
                    self.disable_board()
                    self.play_again()
                else:
                    self.turn = self.p2 if self.turn == self.p1 else self.p1
                    if isinstance(self.turn, ComputerPlayer):
                        root.after(500, self.computer_turn)

    def computer_turn(self):
        self.turn.move()
        if win(self.turn.letter):
            mainLabel.config(text=f"{self.turn.letter} wins!")
            self.disable_board()
            self.play_again()
        elif draw():
            mainLabel.config(text="It's a draw!")
            self.play_again()
        else:
            self.turn = self.p1

    def disable_board(self):
        for i in range(3):
            for j in range(3):
                buttons[i][j].config(state="disabled")

    def play_again(self):
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            enable_buttons()
        else:
            root.quit()

def reset_board():
    global buttons_content, game
    buttons_content = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")
    mainLabel.config(text="Tic Tac Toe")
    game = None

def disable_buttons():
    r1.config(state="disabled")
    r2.config(state="disabled")
    r4.config(state="disabled")
    r5.config(state="disabled")

def enable_buttons():
    r1.config(state="normal")
    r2.config(state="normal")
    r4.config(state="normal")
    r5.config(state="normal")

def start_game():
    global game
    reset_board()
    disable_buttons()

    mainLabel.config(text="Game Started!")
    game_mode = player.get()
    letter = "x" if letter_choice.get() == 1 else "o"
    opponent_letter = "o" if letter == "x" else "x"

    p1 = HumanPlayer(letter)
    p2 = ComputerPlayer(opponent_letter) if game_mode == 1 else HumanPlayer(opponent_letter)
    game = Game(p1, p2)

for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(
            root,
            width=5,
            height=2,
            font=("Pixelify Sans", 35),
            bg=darkPink,
            command=lambda r=row, c=col: game.handle_click(r, c) if game else None
        )
        buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

tk.Label(root, text="Play With:", bg=lightPink, fg=brown, font=("Pixelify Sans", 14, "bold")).grid(row=3, column=0, pady=20)
player = tk.IntVar(value=1)
r1 = tk.Radiobutton(root, text="Computer", image=computerImg, bg=lightPink, fg=brown, font=("Pixelify Sans", 14), variable=player, value=1)
r1.grid(row=3, column=1)
r2 = tk.Radiobutton(root, text="Player 2", image=humanImg, bg=lightPink, fg=brown, font=("Pixelify Sans", 14), variable=player, value=2)
r2.grid(row=3, column=2)

tk.Label(root, text="Letter:", bg=lightPink, fg=brown, font=("Pixelify Sans", 14, "bold")).grid(row=4, column=0, pady=10)
letter_choice = tk.IntVar(value=1)
r4 = tk.Radiobutton(root, text="X", bg=lightPink, fg=brown, font=("Pixelify Sans", 14), variable=letter_choice, value=1)
r4.grid(row=4, column=1)
r5 = tk.Radiobutton(root, text="O", bg=lightPink, fg=brown, font=("Pixelify Sans", 14), variable=letter_choice, value=2)
r5.grid(row=4, column=2)

mainLabel = tk.Label(root, text="Tic Tac Toe", bg=lightPink, fg=brown, font=("Pixelify Sans", 20, "bold"), justify="center")
mainLabel.grid(row=5, column=0, columnspan=3, pady=20)

tk.Button(root, text="Start Game", bg=lightPink, fg=brown, font=("Pixelify Sans", 14), command=start_game).grid(row=6, column=0, columnspan=3, pady=20)

root.mainloop()
