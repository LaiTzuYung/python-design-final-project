from datetime import datetime
import csv
import os

def save_wordle_record(answer, guess_history, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = "wordle_record.csv"
    file_exists = os.path.exists(file_name)

    with open(file_name, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "answer", "result", "guess_count", "guesses"])

        writer.writerow([
            timestamp,
            answer,
            result,
            len(guess_history),
            ";".join(guess_history)
        ])
