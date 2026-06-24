import customtkinter as ctk
import wordSearch
import rankWord
import game
import recordView

class App(ctk.CTk):
    def __init__(self, word_list):
        super().__init__()

        self.btn_game = ctk.CTkButton(self, text="Play Wordle", command=self.open_game)
        self.btn_game.grid(row=5, column=0, padx=10, pady=10)

        self.btn_record = ctk.CTkButton(self, text="View Records", command=self.open_records)
        self.btn_record.grid(row=5, column=1, padx=10, pady=10)

        self.yCount = 0
        self.yellow_rows = [{} for _ in range(5)]
        self.y_labels = [] 
        for i in range(5):
            lbl = ctk.CTkLabel(self, text="", font=("Arial", 40, "bold"), text_color="yellow")
            lbl.place(x=370, y=60 + (i * 50))
            self.y_labels.append(lbl)

        self.gText = ["_", "_", "_", "_", "_"]
        
        self.word_list = word_list
        self.greenDict = {}; self.yellowDict = {}; self.grayDict = set()

        self.title("Wordle Helper")
        self.geometry("600x800")

        # GREEN
        self.entry_g = ctk.CTkEntry(self, placeholder_text="Green (A 1)")
        self.entry_g.grid(row=0, column=0, padx=10, pady=5)
        self.btn_g = ctk.CTkButton(self, text="Add Green", width=100, command=lambda: self.update_data('G'))
        self.btn_g.grid(row=0, column=1, padx=10, pady=5)

        self.label_g1 = ctk.CTkLabel(
            self, 
            text=self.gText, 
            font=("Arial", 40, "bold"), 
            text_color="green"          
        )
        self.label_g1.grid(row=0, column=2, columnspan=2, pady=10)

        # YELLOW
        self.entry_y = ctk.CTkEntry(self, placeholder_text="Yellow (A 2 3)")
        self.entry_y.grid(row=1, column=0, padx=10, pady=5)
        self.btn_y = ctk.CTkButton(self, text="Add Yellow", width=100, command=lambda: self.update_data('Y'))
        self.btn_y.grid(row=1, column=1, padx=10, pady=5)
        
        self.yellow_rows = [{} for _ in range(5)]

        # GRAY
        self.entry_b = ctk.CTkEntry(self, placeholder_text="Gray (Letters)")
        self.entry_b.grid(row=2, column=0, padx=10, pady=5)
        self.btn_b = ctk.CTkButton(self, text="Add Gray", width=100, command=lambda: self.update_data('B'))
        self.btn_b.grid(row=2, column=1, padx=10, pady=5)

        self.gray_display = ctk.CTkLabel(
            self, 
            text="", 
            font=("Arial", 30), 
            text_color="gray",
            wraplength=200   
        )
        self.gray_display.place(x=370, y=310)

        # row 3
        self.btn_s = ctk.CTkButton(self, text="Search", command=self.run_search)
        self.btn_s.grid(row=3, column=0, padx=10, pady=10)
        self.btn_d = ctk.CTkButton(self, text="Reset", command=self.reset_data, fg_color="red")
        self.btn_d.grid(row=3, column=1, padx=10, pady=10)

        # row 4
        self.result_box = ctk.CTkTextbox(self, height=200, width=350)
        self.result_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def update_data(self, mode):
        try:
            if mode == 'G':
                val = self.entry_g.get()
                part = val.split()
                pos = int(part[1])
                letter = part[0]
                wordSearch.parse_green(val, self.greenDict)
                self.gText[pos-1] = letter.upper()
                self.label_g1.configure(text=self.gText)
                self.entry_g.delete(0, 'end')
            elif mode == 'Y':
                val = self.entry_y.get()
                wordSearch.parse_yellow(val, self.yellowDict)

                parts = val.split()
                letter = parts[0].upper()
                positions = set(int(p) for p in parts[1:])

                if self.yCount < 5:
                    if self.yCount == 0:
                        textIni = ["_", "_", "_", "_", "_"]
                        self.yellow_rows[0][letter] = positions
                        for pos in positions:
                            textIni[pos-1] = letter
                        self.y_labels[0].configure(text = textIni)
                        self.y_labels[self.yCount].place(x=370, y=60 + (self.yCount * 50))
                        self.yCount = 1
                    else:
                        found = False
                        for i in range(self.yCount):
                            if(letter in self.yellow_rows[i]):
                                found = True
                                self.yellow_rows[i][letter].update(positions)
                                textIni = ["_", "_", "_", "_", "_"]
                                allPos = self.yellow_rows[i][letter]
                                for pos in allPos:
                                    textIni[pos-1] = letter
                                self.y_labels[i].configure(text = textIni)
                                break

                        if found == False:
                            textIni = ["_", "_", "_", "_", "_"]
                            self.yellow_rows[self.yCount][letter] = positions
                            for pos in positions:
                                textIni[pos-1] = letter
                            self.y_labels[self.yCount].configure(text = textIni)
                            self.y_labels[self.yCount].place(x=370, y=60 + (self.yCount * 50))
                            self.yCount += 1               
                
                self.entry_y.delete(0, 'end')
            elif mode == 'B':
                val = self.entry_b.get()
                wordSearch.parse_gray(val, self.grayDict)
                
                sorted_gray = sorted(list(self.grayDict)) 
                gray_str = " ".join(sorted_gray)          
                self.gray_display.configure(text=gray_str)

                self.entry_b.delete(0, 'end')
        except ValueError as e:
            self.result_box.insert("end", f"Error: {str(e)}\n")
            self.result_box.see("end")
        except Exception as e:
            self.result_box.insert("end", f"Error: {str(e)}\n")

    def run_search(self):
        result = wordSearch.filter_word(self.word_list, self.grayDict, self.greenDict, self.yellowDict)
        bestResult = rankWord.best_guesses(result)
        self.result_box.delete("1.0", "end")
        if len(bestResult)==0:
            self.result_box.insert("1.0", "No valid answer")
        else:
            if len(result)>10:
                self.result_box.insert("end", "Recommended:\n")
                display_list = [word for word, score in bestResult]
                self.result_box.insert("end", "\n".join(display_list))

                self.result_box.insert("end", "\n\nAll results:\n")
                self.result_box.insert("end", "\n".join(result))
            else:
                display_list = [f"{word}" for word, score in bestResult]
                self.result_box.insert("1.0", "\n".join(display_list))

    def reset_data(self):
        self.greenDict = {}
        self.yellowDict = {}
        self.grayDict = set()
        self.yCount = 0
        self.yellow_rows = [{} for _ in range(5)]
        
        self.gText = ["_", "_", "_", "_", "_"]
        self.label_g1.configure(text=self.gText)
        
        for lbl in self.y_labels:
            lbl.configure(text="")
            lbl.place_forget()
            
        self.gray_display.configure(text="")
        
        self.result_box.delete("1.0", "end")

    def open_game(self):
        game.GameWindow(self.word_list)
    
    def open_records(self):
        recordView.RecordWindow(self)


if __name__ == "__main__":
    file_path = r"wordle-list-main\words.txt"
    with open(file_path, "r") as f:
        all_words = [line.strip().upper() for line in f]

    ctk.set_widget_scaling(2) 
    ctk.set_window_scaling(2)
    
    app = App(all_words)
    app.mainloop()