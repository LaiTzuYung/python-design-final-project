"""
單字字典意義查詢工具(Free Dictionary + Merriam-Webster 雙來源版)
讀取一個純文字檔(一行一個單字),依序透過以下兩個來源查詢英文解釋:
    1. Free Dictionary API(免費,不需 key)
    2. Merriam-Webster Collegiate Dictionary API(備援,需自行申請免費 API key)

用法:
    python lookup_words.py 輸入檔.txt

輸出:
    results.txt      -> 查到的單字與解釋(會標明來源)
    not_found.txt    -> 兩個來源都查不到的單字清單
"""

import sys
import time
import requests

# ===================== 設定區 =====================
# 請到 https://dictionaryapi.com/register/index 申請免費帳號,
# 申請時 Select API 選「Collegiate Dictionary」,核准後會 email 給你 API Key。
# 把拿到的 API Key 貼在下面的引號中間。
# 如果先不申請,留空字串 "" 也能跑,只是會跳過 Merriam-Webster 這層備援。
MERRIAM_WEBSTER_API_KEY = "80d46457-bd2b-41bd-9f50-ee527c38f944"

FREE_DICT_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
MW_URL = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}"

DELAY_SECONDS = 0.5  # 每次查詢間隔,避免請求過於密集
# ====================================================


def load_words(filepath):
    """讀取單字清單,去除空白行與重複字(保留原始順序)"""
    seen = set()
    words = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w and w.lower() not in seen:
                seen.add(w.lower())
                words.append(w)
    return words


def lookup_free_dictionary(word):
    """來源 1: Free Dictionary API"""
    try:
        resp = requests.get(FREE_DICT_URL.format(word=word), timeout=10)
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    try:
        data = resp.json()
    except ValueError:
        return None

    if not isinstance(data, list) or len(data) == 0:
        return None

    lines = []
    entry = data[0]
    for meaning in entry.get("meanings", []):
        part_of_speech = meaning.get("partOfSpeech", "")
        definitions = meaning.get("definitions", [])[:2]
        for d in definitions:
            definition_text = d.get("definition", "")
            lines.append(f"  ({part_of_speech}) {definition_text}")

    if not lines:
        return None

    return "\n".join(lines)


def _clean_mw_text(text):
    """去除 Merriam-Webster 回應中的格式標籤,例如 {bc}, {it}word{/it} 等"""
    import re
    # 移除類似 {bc}, {it}, {/it}, {sx|word||} 之類的標記
    text = re.sub(r"\{bc\}", "", text)
    text = re.sub(r"\{/?[a-z_]+\}", "", text)
    text = re.sub(r"\{[a-z_]+\|([^|]*)\|[^}]*\}", r"\1", text)
    return text.strip()


def lookup_merriam_webster(word):
    """來源 2(備援): Merriam-Webster Collegiate Dictionary API,需要 API key"""
    if not MERRIAM_WEBSTER_API_KEY:
        return None

    params = {"key": MERRIAM_WEBSTER_API_KEY}
    try:
        resp = requests.get(MW_URL.format(word=word), params=params, timeout=10)
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    try:
        data = resp.json()
    except ValueError:
        return None

    # Merriam-Webster 查不到完全相符的字時,會回傳「相似字建議」的字串陣列,
    # 而不是字典條目陣列,这种情况也視為查無結果。
    if not isinstance(data, list) or len(data) == 0:
        return None
    if isinstance(data[0], str):
        return None

    lines = []
    for entry in data[:1]:  # 只取第一個條目,避免太長
        # 確認這個條目確實對應到查詢的字(避免抓到不相關的相似字)
        headword = entry.get("meta", {}).get("id", "").split(":")[0]
        if headword.lower() != word.lower():
            continue

        part_of_speech = entry.get("fl", "")
        shortdefs = entry.get("shortdef", [])[:3]
        for d in shortdefs:
            lines.append(f"  ({part_of_speech}) {_clean_mw_text(d)}")

    if not lines:
        return None

    return "\n".join(lines)


def lookup_word(word):
    """
    依序嘗試各來源,回傳 (成功與否, 結果字串或 None, 來源名稱)
    """
    result = lookup_free_dictionary(word)
    if result:
        return True, result, "Free Dictionary"

    result = lookup_merriam_webster(word)
    if result:
        return True, result, "Merriam-Webster"

    return False, None, None


def main():
    if len(sys.argv) < 2:
        print("用法: python lookup_words.py 輸入檔.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    words = load_words(input_path)
    print(f"共讀取到 {len(words)} 個不重複單字,開始查詢...\n")

    if not MERRIAM_WEBSTER_API_KEY:
        print("[提示] 尚未設定 MERRIAM_WEBSTER_API_KEY,本次只會使用 Free Dictionary 查詢。\n")

    found_results = []
    not_found = []

    for i, word in enumerate(words, start=1):
        success, result, source = lookup_word(word)
        if success:
            found_results.append(f"{word}  [來源: {source}]\n{result}\n")
            print(f"[{i}/{len(words)}] {word} -> 查到 ({source})")
        else:
            not_found.append(word)
            print(f"[{i}/{len(words)}] {word} -> 查無結果")

        time.sleep(DELAY_SECONDS)

    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(found_results))

    with open("not_found.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(not_found))

    print(f"\n完成! 查到 {len(found_results)} 個,查無結果 {len(not_found)} 個。")
    print("結果存於 results.txt,查無結果清單存於 not_found.txt")


if __name__ == "__main__":
    main()