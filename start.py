import sys, time, os
from practice import *   # Thanks Derrick for the help :)

def valid(data, Type):      # Checks if input is valid
    if len(data) == 0:
        return False
    for i in data:
        if Type == "userName":     # for username
            if not (i.isdigit() or i.isalpha() or i == "_"):            # if not alphabet, digit or "_" sign
                return False
        if Type == "password":      # for password
            if not(i.isdigit() or i.isalpha() or i in ("! @ # $ % ^ & *").split()):     # if not alphabet, digit or valid signs
                return False
    return True
    
def signUp(Type):       # Sign Up user
    userData = input(": ")
    instruction = {"Username" : "Enter alphabets, numbers or underscores only.", "Password" : "Enter alphabets, numbers and the following symbols only: !,@,#,$,%,^,&,*"}
    while not valid(userData, Type):
        print("Invalid %s" % Type)
        print(instruction[Type])
        print()
        userData = input("%s: " % Type)
    return userData

def readFile(mode):         # reads or writes in a file according to the mode
    if mode == "Sign up":
        if os.path.isfile("userData.txt"):
            with open("userData.txt", "a") as data:
                data.write(userName1+" "+hashPass(password)+" "+vPassword+"\n")
        else:
            with open("userData.txt", "w") as data:
                data.write(userName1+" "+hashPass(password)+" "+vPassword+"\n")
    if mode == "Log in":
        with open("userData.txt", "r") as data:
            userData = []
            rawData = data.readlines()  # reads the file line by line and stores each line as a list
            for line in rawData:
                userData.append(line.split())
            return userData

def encryptUsername(word):  # Encrypts word
    eWord = ""      # encrypted word
    for i in word:
        if ord(i) < 100:    # if the length of ord(i) is 2
            eWord += "0%s" % str(ord(i))
        else:
            eWord += str(ord(i))
    return eWord

def hashPass(password):
    ePass = 0 #encrypted password
    for i in password:
        ePass += ord(i)
    ePass = str(ePass)
    while len(ePass) != 1:
        ePass1 = 0   # temporarily store digits of ePass
        for i in ePass:
            ePass1 += int(i)
        ePass = str(ePass1)
    return ePass

def validatePassOrder(password):    # Created this function because the user was able to log in with the password "cba" even when the true password was "abc".
    # This function checks if the order of words in a password is correct.
    ePass = ""
    for i in password:
        j = list(str(ord(i)))     # Turns ord(i) into string and makes its list.
        j.reverse()     # Reverses it so that we can get its last digit at first place.
        ePass += j[0]                       # stores the first digit (last digit in the actual)
    return ePass

def newUserScore(userName):
    for wordList, text in [["wordList.txt", "mScore.txt"],["synomn.txt", "sScore.txt"],["acronym.txt", "aScore.txt"]]:
        with open(wordList) as file:
            data = file.readlines()
            score = "N"*len(data)
            splitScore = []
            for i in range(0, len(data), grpItems):
                splitScore.append(score[i:i+grpItems])
            line = userName + " " + " ".join(splitScore)
            with open(text, "a") as text:
                text.write(line+"\n")

def scoreBoard():
    for score in ["mScore.txt", "sScore.txt", "aScore.txt"]:
        if score == "mScore.txt":
            print()
            print(" Meaning Mode:")
        if score == "sScore.txt":
            print()
            print(" Synomn Mode:")
        if score == "aScore.txt":
            print()
            print(" Acronym Mode:")
        print()
        print(" Username \t Answer Accuracy (%)")
        with open(score) as file:
            data = file.readlines()
            for line in data:
                line = line.split()
                userName = line[0]
                line.remove(userName)   # removes the user name from the list so that only scores remain
                line = "".join(line)        # Converts list to string
                correct = line.count("C")       # Count correct answers & thanks Aritra for the idea 
                total = correct + line.count("W")   # Count total answers
                if total == 0:
                    print(" %s \t \t Not practiced yet." % userName)
                else:
                    print(" %s \t \t %s %%" % (userName, round((100*correct/total), 2)))

#  - - - - - - - - - - - - - - - - - - Functions end here - - - - - - - - - - - - - - - - - - 

grpItems = 10 # Number of items in one group
while True:
    os.system("cls")
    MODE = {"1" : "Log in", "2" : "Sign up", "3" : "Exit"}
    print()
    print(" Welcome to Vocab! \t \t \t \t Created by: Rgk Rana")
    if not os.path.isfile("userData.txt"):   # if password.txt file not present
        mode = "Sign up"
        print("  Please sign up to start.")
    else:
        print(" 1) Log In \n 2) Sign up \n 3) Exit")
        mode = ""
        while mode not in ("1 2 3").split():
            mode = input(" : ")
        mode = MODE[mode]
    if mode == "Sign up":
        attempts = 0
        checked = False     # To ensure the user confirmed his details
        while not checked:  # While not confirmed
            os.system("cls")
            if attempts == 2:   # Go to start page if not confirmed after 2nd attempt.
                userName = ""
                userName1 = ""
                break
            print()
            print("Sign Up")
            print("- - - -")
            print()
            print("Username ", end = "")
            userName = signUp("Username")
            userName1 = encryptUsername(userName)
            if os.path.isfile("userData.txt"):
                userInfo = readFile("Log in")       # gets usernames and passwords from file
                if userInfo != []:
                    for i in userInfo:
                        if userName1 == i[0]:
                            print("User name '%s' is already used. Please choose another user name." % userName)
                            time.sleep(1)
                            break
                    if userName1 == i[0]:
                        continue
            print("Password", end = "")
            password = signUp("Password")
            print()
            print('''Please confirm your account details:

User name: %s
Password : %s''' % (userName, password))
            attempts += 1
            print()
            if input("Are the details correct? (Y/N) \n").lower().startswith("y"):
                checked = True
        vPassword = validatePassOrder(password)
        if checked:
            readFile(mode)              # Writes encrypted username1 and password to a file
            newUserScore(userName)      # Creates empty score table for new user
        continue
    if mode == "Log in":
        attempts = 0
        validUser = False
        while not validUser:
            os.system("cls")
            userInfo = readFile(mode)
            print()
            print("Log In")
            print("- - - -")
            print()
            userName = input("Username: ")
            password = input("Password: ")
            vPassword = validatePassOrder(password)
            for i, j, k in userInfo:
                if encryptUsername(userName) == i and hashPass(password) == j and vPassword == k:
                    validUser = True
                    break
            if not validUser:
                attempts += 1
                print("Access Denied!")
                print("Invalid user name or password.")
                time.sleep(1)
                if attempts == 3:
                    print("Maximum number of attempts exceeded.")
                    time.sleep(1)
                    break
    if mode == "Exit":
        print()
        print(" Thanks for your time.")
        time.sleep(1)
        sys.exit()
    while validUser:     #Game store after log in
        print("Access Granted!")
        with open("userName.txt", "w") as file:         # Stores the current username in a file so that the username can be received when we import practice
            file.write(userName)
        time.sleep(1)
        print()
        while True:
            choose = ""
            while choose not in ("1 2 3").split():
                os.system("cls")
                print()
                print("Welcome %s!" % userName)
                print("- - - - - - - -")
                print()
                print("1) Practice \n2) Score \n3) Log out")
                choose = input(": ")
            if choose == "1":       # Practice
                os.system("cls")
                main()
            if choose == "2":       # Score
                os.system("cls")
                scoreBoard()
                print()
                input("Press enter to go back . . .")
            if choose == "3":        # Log out
                os.system("cls")
                userName = ""
                break
        if choose == "3":
                break
