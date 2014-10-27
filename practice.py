import os, sys, random, time

def getWordList(mode):
    textFile = {"1" : "wordList.txt", "2":"synonym.txt", "3":"wordList.txt"}
    wordList = []
    with open(textFile[mode]) as file:
        data = file.readlines()
        for line in data:
            if mode == "2":           # For synonym mode
                wordList.append(line.split())
            if mode != "2":           # For meaning and antonym mode
                wordList.append(line.split(":"))     # splits the line at only once in space and divides it into two items i.e word and meaning
        return wordList
    
def groupWords(wordList, grpItems):
    groups = []
    NUM = len(wordList)     # Total number of words
    if 0 < (NUM%grpItems) <= 5:   # If remainder from 1-5
        GNUM = round(NUM / grpItems) +1
    elif (NUM % grpItems) > 5:      # remainder above 5
        GNUM = round(NUM / grpItems)
    else:       #No remainder
        GNUM = round(NUM/10)
    for i in range(0, NUM, grpItems):
        groups.append(wordList[i:i+grpItems])   # Slice items to groups of 'grpItems' items in it
    return groups

def generateAnswers(meaning, grpNum, remove, oldList, mode):    # Generates 4 answer choices and returns position of correct answer
    # I used oldList to keep track of old list of answers used before help asked to make sure the order of new answers don't change.
    if oldList == []:
        selectedAns = [meaning]         # correct meaning
        while True:
            x = random.choice(group[grpNum])        # randomly selects a word and meaning of the same group
            if mode == "1":       # Meaning or Antonym
                if x[1] not in selectedAns:
                    selectedAns.append(x[1])
            if mode == "2":     # Synonyms:
                i = random.randint(0, len(x)-1)
                if x[i] not in selectedAns and meaning not in x:
                    selectedAns.append(x[i])
            if mode == "3":
                if x[2] not in selectedAns:
                    selectedAns.append(x[2])
            if len(selectedAns) == 4:                       # When four options created
                random.shuffle(selectedAns)
                break
        oldList = selectedAns    
    correctAns = ""
    for i in range(len(oldList)):
        if meaning == oldList[i]:
            correctAns = chr(ord("A")+i)
        if chr(ord("A") + i) == remove:         # If skips one wrong option as requested by help
            print("%s)    \n" % (chr(ord("A")+i)))  # prints a line blank if help asked
            continue
        print("%s) %s" % (chr(ord("A")+i), oldList[i]))
    return correctAns, oldList

def askQuestion(grpNum, score, mode):
    helps = 5
    for i in range(len(group[grpNum])): 
        wAns = "A B C D".split()
        ans2remove = ""
        oldSelectedAns = []
        while True:
            os.system("cls")
            if mode == "1":     # Meaning
                word, meaning = group[grpNum][i][0], group[grpNum][i][1]
            if mode == "2": # Synonym
                x, y = 0, 0     # x and y will be used as index for word and meaning
                while x == y:       # Loop until x and y have different integer values
                    x = random.randint(0, len(group[grpNum][i])-1)
                    y = random.randint(0, len(group[grpNum][i])-1)
                word, meaning = group[grpNum][i][x], group[grpNum][i][y]
            else:           # Antonym
                word, meaning = group[grpNum][i][0], group[grpNum][i][2]
            qStatus = status(userName, grpNum, i, score)
            print()
            print("Helps: %s     Status: %s       %s of %s" % ("o"*helps, qStatus, i+1, len(group[grpNum])))
            print()
            print("                    %s        " % word)
            cAns, oldSelectedAns = generateAnswers(meaning, grpNum, ans2remove, oldSelectedAns, mode)         # Correct answer position
            answer = ""
            while answer not in "A B C D".split() and not answer.startswith("HE") and not answer.startswith("SK"):           # if not A, B, C, D or Help
                print("Select answer (A - D) or 'help' to remove one wrong option or 'skip' to skip this question")
                print()
                answer = input(": ").upper()
                if answer == ans2remove:    # if  chosen answer was removed
                    print()
                    print("Option %s is not available." % answer)
                    time.sleep(1)
                    break
            if answer.startswith("SK"):
                print("Question skipped!")
                time.sleep(1)
                updateScore(userName, score, mode, grpNum, i, "S")
                break
            if answer == ans2remove:
                continue
            if answer.startswith("HE"):
                print()
                if len(wAns) == 3:      # Help already used:
                    print("You have already used help for this question.")
                    time.sleep(1)
                    continue
                if helps == 0:
                    print("You have used all help options. No help available.")
                    time.sleep(1)
                    continue
                wAns.remove(cAns)   # remove correct answer from the wrong answers
                ans2remove = random.choice(wAns)
                helps -= 1      # reduce help
                continue                
            if answer == cAns:  # if correct
                updateScore(userName, score, mode, grpNum, i, "C")
                break
            if not answer.startswith("HE") and answer!= cAns and not answer.startswith("SK"):
                updateScore(userName, score, mode, grpNum, i, "W")
                break

def getUserName():      # reads an external file to know the current user 
    with open("userName.txt") as file:
        return file.read()

def getScore():         # Returns the score data from files and convert them into respective variable
    with open("mScore.txt") as file:        
        mScore = []             # Score in meaning mode
        data = file.readlines()
        for line in data:
            mScore.append(line.split())
    with open("sScore.txt") as file:            
        sScore = []             # Score in synonym mode
        data = file.readlines()
        for line in data:
            sScore.append(line.split())
    with open("aScore.txt") as file:
        aScore = []             # Score in antonym mode
        data = file.readlines()
        for line in data:
            aScore.append(line.split())
    return mScore, sScore, aScore

def status(userName, grpNum, qNum, score):  # checks if a question was answered or not and if answered, was it correct or wrong.
    for items in score:
        if userName == items[0]:        # if list of current user
            for i in items[grpNum+1]:
                if items[grpNum+1][qNum-1] == "C":
                    return "Correct"
                if items[grpNum+1][qNum-1] == "W":
                    return "Wrong"
                if items[grpNum+1][qNum-1] == "N":
                    return "Not Done Yet"
                if items[grpNum+1][qNum-1] == "S":
                    return "Skipped"

def calculateScore(score):  # reads mScore, aScore or sScore and calculates score in %
    xScore = []
    for items in score:
        correct, total = 0, 0
        name = item[0]
        for gScore in items:
            if gScore == name:      # skips the first name part of the list
                continue
            for i in gScore:
                if i == "C":
                    correct += 1
                    total += 1
                if i == "W":
                    total += 1
        xScore.append([name, round((100*correct/total), 2)])
    return xScore

def displayScore(List):     # reads the list returned by calculateScore() and display it
    for item in List:
        print(List[0], "  ",List[1], "%")

def updateScore(userName, score, mode, grpNum, qNum, value):     # updates mScore/sScore/aScore and writes them to respective txt file
    for i in score:
        if i[0] != userName:
            continue    # move to another list until we get the score list of current user
        # When the score list of current user is reached
        groupL = list(i[grpNum+1])            # temporarily stores the score of a group
        groupL[qNum] = value            # here value = "C" for correct and "W" for wrong and "N" for not done
        groupL = "".join(groupL)        # Thanks Aritra for the idea
        i[grpNum+1] = groupL
        if mode == "1":
            with open("mScore.txt", "w") as file:
                for a in score:
                    for b in a:
                        file.write(b+" ")
                    file.write("\n")        # breaks line
        if mode == "2":
            with open("sScore.txt", "w") as file:
                for a in score:
                    for b in a:
                        file.write(b+" ")
                    file.write("\n")
        if mode == "3":
            with open("aScore.txt", "w") as file:
                for a in score:
                    for b in a:
                        file.write(b+" ")
                    file.write("\n")

def showTestResult(userName, score, grpNum):
    os.system("cls")
    for i in score:
        correct, total = 0, 0
        if i[0] != userName:
            continue
        print()
        print("Your performance report:")
        print()
        for j in range(len(i[grpNum+1])):
            if i[grpNum+1][j] == "C": # correct
                print("%s) Correct     " % (j+1), end = "  ")
                correct += 1
                total += 1
            if i[grpNum+1][j] == "W": # Wrong
                print("%s) Wrong     " % (j+1), end = " ")
                total += 1
            if i[grpNum+1][j] == "N": # not done yet
                print("%s) Not Done     " % (j+1), end = " ")
            if i[grpNum+1][j] == "S": # skipped
                print("%s) Skipped     " % (j+1), end = " ")
            if j + 1 == len(i[grpNum+1])/2:       # breaks line at when half results printed
                print()
        print()
        if total == 0:
            print()
            print("No result as you skipped all questions.")
        if total != 0:
            print()
            print(str(round(100*correct/total, 2)), "% correct out of ", str(total))
        time.sleep(2)
        print()
        input("Press enter if done with checking your result . . .")

def validGrpNum(num):
    if num.isalpha():
        if num.lower().startswith("ba"):
            return True
    if num.isdigit():
        if int(num) -1 in list(range(grpLen)):
            return True
    return False

def main():
    global grpItems, userName, grpLen, group, mode
    grpItems = 10 # 10 words in each group
    while True:
        os.system("cls")
        userName = getUserName()
        mode = ""
        while mode not in "1 2 3".split() and not mode.lower().startswith("ba"):
            os.system("cls")
            print()
            print("Practice Modes:")
            print("1) Meaning \n2) Synonym \n3) Antonym")
            print()
            mode = input("Select mode or type 'back': ")
        mScore, sScore, aScore = getScore()
        if mode.lower().startswith("ba"):                   # back
            break
        if mode == "1":
            wordList = getWordList(mode)
            group = groupWords(wordList, grpItems)
            grpLen = len(group)
            print()
            print("Select the word group to practice:")
            print()
            while True:
                for i in range(grpLen):
                    if i == 5:      # breaks line after four groups 
                        print()                
                    print("%s) Group %s   " % (i+1, i+1), end = " ")            # prints the available groups.
                print()
                grpNum = ""             # Group number
                while not validGrpNum(grpNum):
                    print()
                    print("Select you group or type 'back'")
                    grpNum = input("Meaning > Group # ")
                    if not validGrpNum(grpNum):
                        print("Invalid Group chosen.")
                        time.sleep(1)
                if grpNum.lower().startswith("ba"):
                    break
                else:
                    grpNum = int(grpNum) - 1
                askQuestion(grpNum, mScore, mode)
                showTestResult(userName, mScore, grpNum)
                break
        if mode == "2":
            wordList = getWordList(mode)
            group = groupWords(wordList, grpItems)
            grpLen = len(group)
            print()
            print("Select the word group to practice:")
            while True:
                for i in range(grpLen):
                    if i +1 == grpLen/2:
                        print()
                        print()
                    print("%s) Group %s   " % (i+1, i+1), end = " ")
                print()
                grpNum = ""
                while not validGrpNum(grpNum):
                    print()
                    print("Select you group or type 'back'")
                    grpNum = input("Synonym > Group # ")
                    if not validGrpNum(grpNum):
                        print("Invalid Group chosen.")
                        time.sleep(1)
                if grpNum.lower().startswith("ba"):
                    break
                else:
                    grpNum = int(grpNum) - 1
                askQuestion(grpNum, sScore, mode)
                showTestResult(userName, sScore, grpNum)
                break
        if mode == "3":
            wordList = getWordList(mode)
            group = groupWords(wordList, grpItems)
            grpLen = len(group)
            print()
            print("Select the word group to practice:")
            while True:
                for i in range(grpLen):
                    if i +1 == grpLen/2:
                        print()
                        print()
                    print("%s) Group %s   " % (i+1, i+1), end = " ")
                print()
                grpNum = ""
                while not validGrpNum(grpNum):
                    print()
                    print("Select you group or type 'back'")
                    grpNum = input("Acronym > Group # ")
                    if not validGrpNum(grpNum):
                        print("Invalid Group chosen.")
                        time.sleep(1)
                if grpNum.lower().startswith("ba"):
                    break
                else:
                    grpNum = int(grpNum) - 1
                askQuestion(grpNum, aScore, mode)
                showTestResult(userName, aScore, grpNum)
                break
