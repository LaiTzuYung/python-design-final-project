"""
letter_frequency.py

讀取字庫檔案（每行一個單字），統計 A~Z 26 個字母在整份字庫中
總共出現的次數（同一個字在一個單字裡出現幾次就算幾次），
畫成長條圖。

使用方式：
    python letter_frequency.py
"""

import string
from collections import Counter

import matplotlib.pyplot as plt

# =========================
# CONFIG（你可以調整的參數）
# =========================
WORD_LIST_PATH = r"C:\Users\a123h\OneDrive\Desktop\pythonProject\wordle-list-main\results.txt"
OUTPUT_IMAGE = "letter_frequency.png"

# 沒找到檔案時的備用字庫（確保程式仍可示範執行）
FALLBACK_WORD_LIST = [
    "CRANE", "SLATE", "TRACE", "ADIEU", "STARE",
    "GRACE", "PLANE", "SOUND", "PIANO", "SMART",
]


def load_word_list(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip().upper() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[警告] 找不到檔案：{path}，改用內建備用字庫（{len(FALLBACK_WORD_LIST)} 字）。")
        return [w.upper() for w in FALLBACK_WORD_LIST]


def count_letters(word_list):
    """統計 A~Z 在所有單字中出現的總次數（含重複字母）。"""
    counter = Counter()
    for word in word_list:
        for ch in word:
            if ch.isalpha():
                counter[ch] += 1

    # 補上次數為 0 的字母，確保 26 個字母都有資料、順序固定 A~Z
    letters = string.ascii_uppercase
    counts = [counter.get(letter, 0) for letter in letters]
    return letters, counts


def plot_letter_frequency(letters, counts, output_path):
    x_positions = range(len(letters))

    plt.figure(figsize=(12, 6))
    bars = plt.bar(x_positions, counts, color="tab:blue", width=0.7)

    plt.xlabel("Letter")
    plt.ylabel("Total occurrences")
    plt.title("Letter Frequency in Word List")
    plt.xticks(list(x_positions), letters)
    plt.grid(True, linestyle="--", alpha=0.4, axis="y")

    # 在每個長條上方標出數字，方便直接讀數值
    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(count),
            ha="center", va="bottom", fontsize=8,
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"圖表已存成：{output_path}")


if __name__ == "__main__":
    word_list = load_word_list(WORD_LIST_PATH)
    letters, counts = count_letters(word_list)

    print("=== 字母出現總次數 ===")
    for letter, count in zip(letters, counts):
        print(f"{letter}: {count}")

    plot_letter_frequency(letters, counts, OUTPUT_IMAGE)