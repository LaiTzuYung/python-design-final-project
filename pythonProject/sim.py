import random
from collections import Counter, defaultdict
from statistics import mean

import matplotlib.pyplot as plt

import wordSearch
import rankWord
import statistics

# =========================
# 你可以調整的參數
# =========================
N_TRIALS = 5000
MAX_GUESSES = 6

# =========================
# Wordle 回饋計算
# =========================
def average_round_counts(all_round_counts, max_guesses=6):
    result = []
    for round_idx in range(max_guesses):
        values = []
        for game_counts in all_round_counts:
            if round_idx < len(game_counts):
                values.append(game_counts[round_idx])
        result.append(mean(values) if values else 0)
    return result

def plot_round_counts(random_result, high_score_result):
    x = list(range(1, MAX_GUESSES + 1))

    random_avg = average_round_counts(random_result["all_round_counts"], MAX_GUESSES)
    high_avg = average_round_counts(high_score_result["all_round_counts"], MAX_GUESSES)

    plt.figure(figsize=(8, 5))
    plt.plot(x, random_avg, marker="o", label="Random Strategy")
    plt.plot(x, high_avg, marker="o", label="High Score Strategy")

    plt.xlabel("Guess Round")
    plt.ylabel("Average Candidate Count")
    plt.title("Average Remaining Candidates by Round")
    plt.xticks(x)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def print_summary(result):
    print(f"=== {result['strategy'].upper()} Strategy ===")
    print(f"Trials: {result['n_trials']}")
    print(f"Success: {result['success_count']}")
    print(f"Failure: {result['failure_count']}")
    print(f"Success Rate: {result['success_rate']:.4f}")
    print(f"Failure Rate: {result['failure_rate']:.4f}")
    print(f"Avg Guess: {result['avg_guess']}")


def get_feedback(guess, answer):
    """
    回傳一個長度 5 的 feedback:
    G = green
    Y = yellow
    B = gray/black
    """
    answer_count = Counter(answer)
    green = {}
    yellow = {}
    gray = set()
    marked = [False] * 5

    # 先標 green
    for i in range(5):
        if guess[i] == answer[i]:
            green[i + 1] = guess[i]
            answer_count[guess[i]] -= 1
            marked[i] = True

    # 再標 yellow
    for i in range(5):
        if not marked[i] and answer_count.get(guess[i], 0) > 0:
            yellow.setdefault(guess[i], set()).add(i + 1)
            answer_count[guess[i]] -= 1
            marked[i] = True

    # 剩下 gray
    for i in range(5):
        if not marked[i]:
            gray.add(guess[i])
    return green, yellow, gray

def merge_feedback(total_green, total_yellow, total_gray, green, yellow, gray):
    total_green.update(green)
    for letter, positions in yellow.items():
        if letter in total_yellow:
            total_yellow[letter].update(positions)
        else:
            total_yellow[letter] = set(positions)
    total_gray.update(gray)

# =========================
# 選字策略
# =========================
def choose_random_candidate(candidate_list):
    return random.choice(candidate_list)


def choose_high_score_candidate(candidate_list):
    ranked = rankWord.best_guesses(candidate_list, top_n=1)
    return ranked[0][0]


# =========================
# 模擬一局
# =========================
def simulate_game(answer, strategy, word_list):
    candidate_list = word_list[:]
    guesses = []
    rounds_candidate_count = []
    total_green = {}
    total_yellow = {}
    total_gray = set()

    for turn in range(1, MAX_GUESSES + 1):
        rounds_candidate_count.append(len(candidate_list))

        if not candidate_list:
            return {
                "success": False,
                "guess_count": turn - 1,
                "guesses": guesses,
                "rounds_candidate_count": rounds_candidate_count
            }

        if strategy == "random":
            guess = choose_random_candidate(candidate_list)
        elif strategy == "high_score":
            guess = choose_high_score_candidate(candidate_list)
        else:
            raise ValueError("Unknown strategy")

        guesses.append(guess)

        if guess == answer:
            return {
                "success": True,
                "guess_count": turn,
                "guesses": guesses,
                "rounds_candidate_count": rounds_candidate_count
            }

        green, yellow, gray = get_feedback(guess, answer)
        merge_feedback(total_green, total_yellow, total_gray, green, yellow, gray)

        candidate_list = wordSearch.filter_word(candidate_list, total_gray, total_green, total_yellow)

    return {
        "success": False,
        "guess_count": MAX_GUESSES,
        "guesses": guesses,
        "rounds_candidate_count": rounds_candidate_count
    }



# =========================
# 跑多次模擬
# =========================
def run_simulation(n_trials, strategy, word_list, answers):
    success_count = 0
    failure_count = 0
    total_guess_count = 0
    all_round_counts = []

    for i in range(n_trials):
        answer = answers[i]
        result = simulate_game(answer, strategy, word_list)

        if result["success"]:
            success_count += 1
            total_guess_count += result["guess_count"]
        else:
            failure_count += 1

        all_round_counts.append(result["rounds_candidate_count"])

    success_rate = success_count / n_trials
    failure_rate = failure_count / n_trials
    avg_guess = total_guess_count / success_count if success_count > 0 else None

    return {
        "strategy": strategy,
        "n_trials": n_trials,
        "success_count": success_count,
        "failure_count": failure_count,
        "success_rate": success_rate,
        "failure_rate": failure_rate,
        "avg_guess": avg_guess,
        "all_round_counts": all_round_counts
    }


# =========================
# 主程式
# =========================
if __name__ == "__main__":
    random.seed(906198)

    file_path = r"wordle-list-main\words.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        all_words = [line.strip().upper() for line in f if line.strip()]

    answers = [random.choice(all_words) for _ in range(N_TRIALS)]

    random_result = run_simulation(N_TRIALS, "random", all_words, answers)
    high_score_result = run_simulation(N_TRIALS, "high_score", all_words, answers)

    print_summary(random_result)
    print()
    print_summary(high_score_result)

    plot_round_counts(random_result, high_score_result)

