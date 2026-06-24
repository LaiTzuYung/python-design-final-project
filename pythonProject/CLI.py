import wordSearch

greenDict = {}
yellowDict = {}
grayDict = set()

file_path = r"wordle-list-main\words"
all_word = []
with open(file_path, 'r') as fp:
    data = fp.readlines()
    for line in data:
        word = line.upper().strip()
        all_word.append(word)

print("")

while(True):
    status = input("Enter command:").upper()

    match status:
        case 'G':
            while(True):
                try:
                    line = input("Enter green letter:").upper()
                    if line.strip() == "":
                        break
                    letter, pos = line.split()
                    greenDict[int(pos)] = letter
                except:
                    print("Wrong format")
        case 'Y':
            while(True):
                try:
                    yellow = input("Enter yellow letter").upper()
                    if yellow == "":
                        break
                    yellow = yellow.split()
                    letter = yellow[0]
                    pos = yellow[1:]
                    posS = set(map(int, pos))
                    if letter in yellowDict:
                        yellowDict[letter].update(posS) 
                    else:
                        yellowDict[letter] = posS 
                except:
                    print("Wrong format")
        case 'B':
            while(True):
                try:
                    badWord = input("Enter black letter").upper()
                    if(badWord==""):
                        break
                    for char in badWord.split():
                        grayDict.add(char)
                except:
                    print("Wrong format")
        case 'S':
            result = wordSearch.filter_word(all_word, grayDict, greenDict, yellowDict)
            print(result)
        case 'D':
            greenDict = {}
            yellowDict = {}
            grayDict = set()
        case 'R':
            record = input("Enter word to be stored:").upper()
            if record != "":
                with open("wordRecord.txt", 'a') as f:
                    f.write(record + '\n')
                print(f"{record} stored to wrodRecord.txt")
        case 'Q':
            break