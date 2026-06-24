def is_valid(word, gray, green, yellow, valid_letter):
    wordLetterCount = {}
    for char in word:
        if char in wordLetterCount:
            wordLetterCount[char] += 1
        else:
            wordLetterCount[char] = 1
    
    for pos in green:
        if(word[pos-1]!=green[pos]):
            return False
    
    for letter in yellow:
        if letter not in word:
            return False
        for pos in yellow[letter]:
            if word[pos-1] == letter:
                return False
            
    required = {}
    for char in green.values():
        required[char] = required.get(char, 0) + 1
    for char in yellow:
        required[char] = required.get(char, 0) + 1

    for char in gray:
        if char not in valid_letter:
            if char in word:
                return False
        else:
            if wordLetterCount.get(char, 0) > required.get(char, 0):
                return False
            
    return True

def filter_word(word_list, gray, green, yellow):
    filtered = []
    valid_letter = set(green.values()) | set(yellow.keys())
    for word in word_list:
        if is_valid(word, gray, green, yellow, valid_letter):
            filtered.append(word)
    return filtered

def parse_green(green_str, greenDict):
    parts = green_str.split()
    if(len(parts) != 2 or not parts[0].isalpha() or len(parts[0]) != 1 or not parts[1].isdigit()):
        raise ValueError("Green wrong format。correct format:{letter}  {number 1~5}")
    letter = parts[0]
    pos = int(parts[1])
    if pos > 5 or pos <= 0:
        raise ValueError("Green wrong format。correct format:{letter}  {number 1~5}")
    greenDict[pos] = letter.upper()
    return greenDict

def parse_yellow(yellow_str, yellowDict):
    parts = yellow_str.split()
    if len(parts) < 2 or not parts[0].isalpha() or len(parts[0]) != 1:
        raise ValueError("Yellow wrong format。correct format:{letter}  {numbers 1~5}")
    letter = parts[0].upper()
    try:
        posS = set(map(int, parts[1:]))
    except ValueError:
        raise ValueError("Yellow wrong format。correct format:{letter}  {numbers 1~5}")
    
    for p in posS:
        if p > 5 or p < 1:
            raise ValueError("Yellow wrong format。correct format:{letter}  {numbers 1~5}")
        
    if letter in yellowDict:
        yellowDict[letter].update(posS)
    else:
        yellowDict[letter]=posS

    return yellowDict

def parse_gray(gray_str, graySet):
    gray = gray_str.replace(" ", "").strip()
    if not gray:
        return graySet
    
    new_gray = set(gray.upper())
    for char in new_gray:
        if not char.isalpha():
            raise ValueError(f"Gray error:'{char}' not a valid letter")

    graySet.update(new_gray)
    return graySet
