import customtkinter as ctk
import csv
import os

class RecordWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Wordle Records")
        self.geometry("400x500")

        self.file_name = "wordle_record.csv"
        self.records = []

        # 標題
        self.title_label = ctk.CTkLabel(
            self,
            text="Wordle Records",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=10)

        self.list_frame = ctk.CTkScrollableFrame(self, height=150) 
        self.list_frame.pack(padx=10, pady=5, fill="x") 


        self.detail_frame = ctk.CTkFrame(self) 
        self.detail_frame.pack(padx=10, pady=10, fill="both", expand=True) 

        self.detail_text = ctk.CTkTextbox(self.detail_frame) 
        self.detail_text.pack(padx=10, pady=10, fill="both", expand=True)

        # 底部按鈕
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=5)

        self.reload_btn = ctk.CTkButton(self.btn_frame, text="Reload", command=self.load_records)
        self.reload_btn.pack(side="left", padx=10)

        self.close_btn = ctk.CTkButton(self.btn_frame, text="Close", command=self.destroy)
        self.close_btn.pack(side="left", padx=10)

        self.load_records()

    def load_records(self):
        # 清空舊內容
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.detail_text.delete("1.0", "end")
        self.detail_text.insert("end", "Select a record to view details\n")

        self.records = []

        if not os.path.exists(self.file_name):
            no_file_label = ctk.CTkLabel(self.list_frame, text="No record file found.")
            no_file_label.pack(pady=10)
            return

        with open(self.file_name, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.records = list(reader)

        if not self.records:
            no_data_label = ctk.CTkLabel(self.list_frame, text="No records yet.")
            no_data_label.pack(pady=10)
            return

        for idx, record in enumerate(self.records, 1):
            answer = record.get("answer", "")
            result = record.get("result", "")
            guess_count = record.get("guess_count", "")
            timestamp = record.get("timestamp", "")

            summary_text = f"{idx}. {timestamp} | {result} | {guess_count} guesses | Answer: {answer}"

            btn = ctk.CTkButton(
                self.list_frame,
                text=summary_text,
                anchor="w",
                command=lambda r=record, i=idx: self.show_detail(r, i)
            )
            btn.pack(fill="x", padx=5, pady=3)

    def show_detail(self, record, idx):
        self.detail_text.delete("1.0", "end")

        timestamp = record.get("timestamp", "")
        answer = record.get("answer", "")
        result = record.get("result", "")
        guess_count = record.get("guess_count", "")
        guesses = record.get("guesses", "")

        detail = (
            f"Record #{idx}\n"
            f"{'-' * 30}\n"
            f"Timestamp: {timestamp}\n"
            f"Answer: {answer}\n"
            f"Result: {result}\n"
            f"Guess Count: {guess_count}\n"
            f"Guesses:\n"
        )

        for i, g in enumerate(guesses.split(";"), 1):
            if g.strip():
                detail += f"  {i}. {g.strip()}\n"

        self.detail_text.insert("end", detail)
