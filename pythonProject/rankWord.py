from collections import Counter

def letter_frequencies(word_list):
    all_letters = "".join(word_list)
    return Counter(all_letters)

def score_word(word, frequencies):
    unique_chars = set(word)
    score = sum(frequencies[char] for char in unique_chars)
    return score

def best_guesses(word_list, top_n=10):
    freqs = letter_frequencies(word_list)

    scored_list = [(word, score_word(word, freqs)) for word in word_list]

    scored_list.sort(key=lambda x: x[1], reverse=True)
    return scored_list[:top_n]