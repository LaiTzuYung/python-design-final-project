import customtkinter as ctk
import random
from collections import Counter
import gameLog

class GameWindow(ctk.CTkToplevel):
    def __init__(self, word_list):
        super().__init__()
        self.word_list = word_list
        self.title("Wordle Game")
        self.geometry("400x500")
        self.answer = random.choice(word_list).upper()
        self.guess_history = []


        self.guessesCount = 0
        self.grid = []

        for r in range(6):
            row_labels = []
            for c in range(5):
                lbl = ctk.CTkLabel(
                    self,
                    text="_",
                    font=("Arial", 30, "bold"),
                    width=40,
                    height=40,
                    fg_color="white"
                )
                lbl.place(x=80 + (c * 50), y=80 + (r * 50))
                row_labels.append(lbl)
            self.grid.append(row_labels)

        
        self.entry = ctk.CTkEntry(self, width=200, height=40, placeholder_text="Enter 5-letter word")
        self.entry.place(x=40, y=20)
        
        self.btn = ctk.CTkButton(self, width=80, height=40, text="Submit", command=self.submit_guess)
        self.btn.place(x=250, y=20)

        self.reset_btn = ctk.CTkButton(self, width=40, height=40, text="R", command=self.reset_game, fg_color="red")
        self.reset_btn.place(x=350, y=20)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 35))
        self.result_label.place(x=80, y=400)

    def submit_guess(self):
        if self.guessesCount >= 6: return
        guess = self.entry.get().upper()
        if len(guess) != 5 :
            self.result_label.configure(text="Please enter 5 letters")
            return
        if not guess.isalpha():
            self.result_label.configure(text="Only English letters allowed")
            return
        
        self.entry.delete(0, 'end')
        self.entry.focus()
        
        answer_count = Counter(self.answer)
        rows = self.grid[self.guessesCount]

        marked = [False]*5 
        
        for i in range(5):
            if guess[i] == self.answer[i]:
                rows[i].configure(text=guess[i], fg_color="green")
                answer_count[guess[i]] -= 1
                marked[i] = True
        
        for i in range(5):
            if not marked[i]:
                if guess[i] in self.answer and answer_count[guess[i]] > 0:
                    rows[i].configure(text=guess[i], fg_color="yellow")
                    answer_count[guess[i]] -= 1
                    marked[i] = True
        
        for i in range(5):
            if not marked[i]:
                rows[i].configure(text=guess[i], fg_color="gray")
        self.guessesCount += 1
        self.guess_history.append(guess)
        if guess == self.answer:
            self.result_label.configure(text="You Win!")
            self.btn.configure(state="disabled")
            gameLog.save_wordle_record(self.answer, self.guess_history, "WIN")
        elif self.guessesCount == 6:
            self.result_label.configure(text=f"Game Over!\n{self.answer}")
            self.btn.configure(state="disabled")
            gameLog.save_wordle_record(self.answer, self.guess_history, "LOSE")

    def reset_game(self):
        self.answer = random.choice(self.word_list).upper()
        self.guessesCount = 0
        self.result_label.configure(text="")
        self.btn.configure(state="normal")
        self.entry.delete(0, "end")
        self.guess_history = []

        for r in range(6):
            for c in range(5):
                self.grid[r][c].configure(text="_", fg_color="white")
        self.entry.focus()
