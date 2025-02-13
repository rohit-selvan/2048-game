import tkinter as tk
import random
import time
import winsound  

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("2048 Game")
        self.master.geometry("500x650")
        self.configure(bg="#bbada0")
        self.pack(fill="both", expand=True)  
        self.create_GUI()
        self.start_game()
        self.master.bind("<Key>", self.key_press)
        self.encouragements = ["Great Move!", "Keep it up!", "You're on fire!", "Awesome!", "Go for 2048!"]
        self.mainloop()

    def create_GUI(self):
        # Title at the top
        self.title_label = tk.Label(self, text="2048 Game", font=("Verdana", 36, "bold"), bg="#bbada0", fg="#f9f6f2")
        self.title_label.pack(pady=10)
        
        # Main grid centered in the frame
        self.main_grid = tk.Frame(self, bg="#bbada0", bd=3)
        self.main_grid.pack(pady=20)
        
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg="#cdc1b4",
                    width=100,
                    height=100
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(cell_frame, bg="#cdc1b4", fg="#776e65", font=("Verdana", 24, "bold"), width=4, height=2)
                cell_number.pack(expand=True)
                row.append(cell_number)
            self.cells.append(row)
        
        # Score at the bottom
        self.score_label = tk.Label(self, text="Score: 0", font=("Verdana", 24, "bold"), bg="#bbada0", fg="white")
        self.score_label.pack(pady=10)
        
        self.message_label = tk.Label(self, text="", font=("Verdana", 18, "italic"), bg="#bbada0", fg="white")
        self.message_label.pack(pady=10)

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.update_GUI()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j].configure(text="", bg="#cdc1b4")
                else:
                    self.cells[i][j].configure(
                        text=str(cell_value), 
                        bg=self.get_color(cell_value), 
                        fg=self.get_text_color(cell_value)
                    )
        self.score_label.configure(text=f"Score: {self.score}")
        self.message_label.configure(text=random.choice(self.encouragements) if self.score > 0 and self.score % 100 == 0 else "")
        self.update_idletasks()

    def get_color(self, value):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def get_text_color(self, value):
        return "white" if value >= 8 else "#776e65"

    def key_press(self, event):
        key = event.keysym
        if key in ('Up', 'Down', 'Left', 'Right'):
            if self.move(key):
                self.add_new_tile()
                self.update_GUI()
                if self.check_game_over():
                    self.game_over()

    def move(self, direction):
        def merge(row):
            merged = []
            for i in range(3):
                if row[i] != 0 and row[i] == row[i + 1] and i not in merged:
                    row[i] *= 2
                    self.score += row[i]
                    self.play_sound("merge")
                    row[i + 1] = 0
                    merged.append(i)
            new_row = [num for num in row if num != 0]
            return new_row + [0] * (4 - len(new_row))

        moved = False
        for i in range(4):
            if direction in ('Up', 'Down'):
                col = [self.matrix[x][i] for x in range(4)]
                if direction == 'Down':
                    col.reverse()
                merged_col = merge(col)
                if direction == 'Down':
                    merged_col.reverse()
                for x in range(4):
                    if self.matrix[x][i] != merged_col[x]:
                        moved = True
                        self.matrix[x][i] = merged_col[x]
            else:
                row = self.matrix[i]
                if direction == 'Right':
                    row.reverse()
                merged_row = merge(row)
                if direction == 'Right':
                    merged_row.reverse()
                if self.matrix[i] != merged_row:
                    moved = True
                    self.matrix[i] = merged_row
        return moved

    def check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    return False
                if i < 3 and self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False
                if j < 3 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
        return True

    def game_over(self):
        self.play_sound("gameover")
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            game_over_frame,
            text="Game Over",
            bg="#bbada0",
            fg="white",
            font=("Verdana", 48, "bold")
        ).pack()

    def play_sound(self, sound_type):
        if sound_type == "merge":
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        elif sound_type == "gameover":
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

if __name__ == "__main__":
    Game2048()
