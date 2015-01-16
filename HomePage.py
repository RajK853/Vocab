import sys
import time
import pygame
import random
import os
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

# Window setup
WINW = WINH = 550
windowSurface = pygame.display.set_mode((WINW, WINH))
pygame.display.set_caption("Vocab")

# Background Music
pygame.mixer.music.load("Data/Cavin_Harris_Summer.mp3")
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True  # Keeps track of whether background music is playing or not
musicRect = pygame.Rect(20, 20, 20, 20)  # Rectangle to draw music logo

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)  # Custom color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
SILVER = (192, 192, 192)
# Colors for progress bar
DDARK = (50, 50, 200)
DARK = (100, 100, 200)
MID = (150, 150, 200)
LIGHT = (200, 200, 200)

# Unicode for keyboard keys
SHIFT = [304, 303]  # Left and Right Shift
CTRL = [305, 306]  # Left and Right Ctrl
ALT = [307, 308]  # Left and Right Alt
ENTER = 13
TAB = 9

# Set up constants for progress bar
Gap = g = 5  # Gap between the circles
EmptySlots = e = 9  # Number of empty circles used for progress bar
Radius = r = 10  # Radius of each circle

# Constants of the program
grpItems = 10  # Number of words in each group
startupCheck = True     # If True, checks the program data for any error or invalid format

def makeLogo():  # Make the logo
    global logoRect
    logo = pygame.image.load("Data/logo.png")
    stretchedLogo = pygame.transform.scale(logo, (int(WINW / 2.5), int(WINH / 2.5)))
    logoRect = stretchedLogo.get_rect()
    logoRect.left = WINW * 0.3
    logoRect.top = 20
    windowSurface.blit(stretchedLogo, logoRect)

def drawEmptyBar():  # draw empty white cirlces for progress bar
    for i in range(EmptySlots):
        pygame.draw.circle(windowSurface, WHITE, (round((WINW-e*2*r-(e-1)*g)/2)+r+i*(2*r+g), r+logoRect.bottom+15), r, 1)

def progressBar(time, text):  # Draws the progress bar
    for l in range(time):  # Limiting the looping number
        bColor = [LIGHT, MID, DARK, DDARK]
        for i in range(EmptySlots):
            windowSurface.fill(BLACK)
            makeLogo()
            textRect = pygame.font.SysFont("Comic Sans MS", 18,True).render(text, True, WHITE, BLACK).get_rect()
            textRect.centerx = windowSurface.get_rect().centerx
            textRect.top = logoRect.bottom+30+r
            writeText(text, WHITE, textRect, 18, False)
            # Make the progress bar
            drawEmptyBar()
            for c in range(len(bColor)):
                x = i + c
                if x >= EmptySlots:
                    x = len(bColor) - (c + 1)
                pygame.draw.circle(windowSurface, bColor[c], (round((WINW - e * 2 * r - (e - 1) * g) / 2 + r + x * (2 * r + g)), r + logoRect.bottom + 15), r - 1, 0)
            pygame.display.update()
            mainClock.tick(10)

def writeText(text, color, rect, size, returnTextInfo):  # Writes text in the following rect coordinates
    font = pygame.font.SysFont("Comic Sans MS", size, True)
    textObj = font.render(text, True, color, BLACK)
    textRect = textObj.get_rect()
    textRect.left = rect.left
    textRect.top = rect.top
    windowSurface.blit(textObj, textRect)
    if returnTextInfo:  # If returnTextInfo == True
        return textRect

def textBox(text, top):  # Makes a textbox
    font = pygame.font.SysFont("Comic Sans MS", 16)
    textObj = font.render(text, True, WHITE, BLACK)
    textRect = textObj.get_rect()
    textRect.topleft = (WINW/4, top)
    textRect.size = (WINW/2, 25)
    windowSurface.blit(textObj, textRect)
    pygame.draw.rect(windowSurface, WHITE, (textRect.left - 2, textRect.top, textRect.width + 2, textRect.height), 1)
    return textRect

def highlight(rect, color):  # Highlights the rect rectangle
    pygame.draw.rect(windowSurface, color, (rect.left - 2, rect.top - 1, rect.width + 2, rect.height + 1), 2)

def button(text, highlightStatus, rect, button):  # Makes a button with text written on the button, highlight status, rect with information of the button be drawn and button to highlight
    font = pygame.font.SysFont("Comic Sans MS", 22, True)
    textObj = font.render(text, True, WHITE)
    textRect = textObj.get_rect()
    textRect.topleft = (rect.left, rect.bottom + 10)
    textRect.height = 30
    if highlightStatus == button:
        image = pygame.image.load("Data/button2.png")
    else:
        image = pygame.image.load("Data/button1.png")
    stretchedImage = pygame.transform.scale(image, (textRect.width + 6, 33))
    windowSurface.blit(stretchedImage, (textRect.left - 3, textRect.top, textRect.width, textRect.height))
    windowSurface.blit(textObj, textRect)
    return textRect

def readFile(mode, userName, password):  # reads or writes in a file according to the mode
    if mode == "Sign up":
        if os.path.isfile("Data/userData.txt"):     # if file present, append in it
            with open("Data/userData.txt", "a") as data:
                data.write(
                    encryptUsername(userName) + " " + hashPass(password) + " " + validatePassOrder(password) + "\n")
        else:       # if file not present, make new file
            with open("Data/userData.txt", "w") as data:
                data.write(
                    encryptUsername(userName) + " " + hashPass(password) + " " + validatePassOrder(password) + "\n")
    if mode == "Log in":
        with open("Data/userData.txt", "r") as data:
            rawData = data.readlines()  # reads the file line by line and stores each line as a list
            userData = [line.split() for line in rawData]
            if userData == []:
                return [["", "", ""]]
            return userData

def error(rect):  # Display a error sign beside the invalid input
    errorImg = pygame.image.load("Data/error.png")
    stretchedImg = pygame.transform.scale(errorImg, (25, 25))
    errorRect = stretchedImg.get_rect()
    errorRect.topleft = (rect.right+5, rect.top)
    windowSurface.blit(stretchedImg, errorRect)

def board(text, password, HIGHLIGHT, SELECTED, mode, musicPlaying, startupCheck):  # Makes a board with username and password textbox
    i = 0
    userInfo = readFile("Log in", text, password)  # retrieves user data (existing username and hash passwords) from the external file
    while True:
        windowSurface.fill(BLACK)
        makeLogo()
        musicLogo(musicPlaying, musicRect)
        if i == 3:  # If maximum number of attempts exceeded
            font = pygame.font.SysFont("Comic Sans MS", 20, True)
            textObj = font.render("Maximum number of attempts exceeded!", True, RED, BLACK)
            textRect = textObj.get_rect()
            textRect.centerx = windowSurface.get_rect().centerx
            textRect.top = logoRect.bottom + 10
            windowSurface.blit(textObj, textRect)
            pygame.display.update()
            time.sleep(2)
            homepage(musicPlaying, startupCheck)
        username = textBox(text, logoRect.bottom + 10)  # Username textbox
        ePass = "#" * len(password)  # Show password as #s
        if password == "Password":
            passRect = textBox("Password", username.bottom + 5)  # in default fill the password textbox with 'password' text
        else:
            passRect = textBox(ePass, username.bottom + 5)  # show password as # in password textbox
        if mode == "Log in":
            submit = button("Submit", HIGHLIGHT, pygame.Rect(200, passRect.top, 50, passRect.height), [True, "s"])  # make a submit button for Log In
        elif mode == "Sign up":
            submit = button("Create", HIGHLIGHT, pygame.Rect(200, passRect.top, 50, passRect.height), [True, "s"])  # else make a create button for Sign Up
        back = button("Back", HIGHLIGHT, pygame.Rect(submit.right + 10, passRect.top, 40, passRect.height), [True, "b"])  # make a back button
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse motion event
            if event.type == MOUSEMOTION:
                x, y = event.pos
                if username.colliderect((x, y, 0, 0)):  # Cursor over username textbox
                    HIGHLIGHT = [True, "u"]
                elif passRect.colliderect((x, y, 0, 0)):  # Cursor over the password textbox
                    HIGHLIGHT = [True, "p"]
                elif submit.colliderect((x, y, 0, 0)):  # Cursor over the submit button
                    HIGHLIGHT = [True, "s"]
                elif back.colliderect((x, y, 0, 0)):  # Cursor over the back button
                    HIGHLIGHT = [True, "b"]
                else:  # Cursor over the blank space of the window
                    HIGHLIGHT = [False, "n"]
            # mouse click event
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if musicRect.colliderect((x, y, 0, 0)):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                elif username.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = SELECTED = [True, "u"]
                    if text == "Username":
                        # empty the username field for user to type
                        text = ""
                    if password == "":
                        # if password field is empty, fill it with the text 'Password'
                        password = "Password"
                elif passRect.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = SELECTED = [True, "p"]
                    if password == "Password":
                        # Empty the password field for user to type
                        password = ""
                    if text == "":
                        # if username field is empty, fill it with the text 'Username'
                        text = "Username"
                elif submit.colliderect((x, y, 0, 0)):
                    # If submit button clicked
                    HIGHLIGHT = [True, "s"]
                    if password == "Password" or password == "":
                        # not a valid password
                        error(passRect)
                        password = "Password"
                    if text == "Username" or text == "":
                        # not a valid username
                        error(username)
                        text = "Username"
                    if password == "Password" or password == "" or text == "Username" or text == "":
                        pygame.display.update()
                        i += 1
                        time.sleep(2)  # show the error symbol for 2 seconds in the screen
                    else:
                        if mode == "Sign up":
                            for info in userInfo:
                                if encryptUsername(text) == info[0]:  # If username already exists
                                    writeText("Username exists!", RED, pygame.Rect(username.right + 10, username.top, 0, 0), 15, False)
                                    i += 1
                                    pygame.display.update()
                                    time.sleep(1.5)
                                    break
                            if encryptUsername(text) == info[0]:  # If username already exists
                                continue
                            else:
                                checked = False
                                while not checked:
                                    windowSurface.fill(BLACK)
                                    makeLogo()
                                    writeText("Please confirm your username and password.", WHITE, pygame.Rect(logoRect.left - 50, logoRect.bottom + 10, 0, 0), 15, False)
                                    writeText("Username:", WHITE, pygame.Rect(logoRect.left - 30, logoRect.bottom + 30, 0, 0), 15, False)
                                    writeText(text, BLUE, pygame.Rect(logoRect.left + 50, logoRect.bottom + 30, 0, 0), 18, False)
                                    writeText("Password:", WHITE, pygame.Rect(logoRect.left - 30, logoRect.bottom + 55, 0, 0), 15, False)
                                    writeText(password, BLUE, pygame.Rect(logoRect.left + 50, logoRect.bottom + 55, 0, 0), 18, False)
                                    OK = button("OK", HIGHLIGHT, pygame.Rect(logoRect.left + 50, logoRect.bottom + 90, 0, 0), [True, "o"])
                                    Cancel = button("Cancel", HIGHLIGHT, pygame.Rect(OK.right + 10, logoRect.bottom + 90, 0, 0), [True, "c"])
                                    # event handling
                                    for event in pygame.event.get():
                                        if event.type == QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == MOUSEMOTION:
                                            x, y = event.pos
                                            if OK.colliderect((x, y, 0, 0)):
                                                HIGHLIGHT = [True, "o"]
                                            elif Cancel.colliderect((x, y, 0, 0)):
                                                HIGHLIGHT = [True, "c"]
                                            else:
                                                HIGHLIGHT = [False, "n"]
                                        if event.type == MOUSEBUTTONDOWN:
                                            x, y = event.pos
                                            if OK.colliderect((x, y, 0, 0)):
                                                HIGHLIGHT = [True, "o"]
                                                readFile(mode, text, password)
                                                newUserScore(text)
                                                progressBar(2, "Creating your account. . .")
                                                homepage(musicPlaying, startupCheck)
                                            elif Cancel.colliderect((x, y, 0, 0)):
                                                HIGHLIGHT = [True, "c"]
                                                signUp(musicPlaying, startupCheck)
                                            else:
                                                HIGHLIGHT = [False, "n"]
                                    pygame.display.update()
                        elif mode == "Log in":
                            userInfo = readFile(mode, text, password)
                            for info in userInfo:
                                if encryptUsername(text) == info[0] and hashPass(password) == info[1] and validatePassOrder(password) == info[2]:
                                    progressBar(1, "Access Granted!")
                                    return text, musicPlaying  # returns username and current status of music
                            if [encryptUsername(text), hashPass(password), validatePassOrder(password)] not in userInfo:
                                tempRect = pygame.draw.rect(windowSurface, BLACK, (submit.left - 50, submit.top, 200, 50))  # Draw a white rectangle over the submit and back buttons
                                writeText("Invalid Username or Password!", RED, tempRect, 17, False)
                                i += 1
                                pygame.display.update()
                                time.sleep(1)
                elif back.colliderect((x, y, 0, 0)):  # Cursor over the back button
                    # If back button clicked
                    HIGHLIGHT = [True, "b"]
                    homepage(musicPlaying, startupCheck)
                else:       # if clicked at blank space around
                    if text == "":
                        text = "Username"
                    if password == "":
                        password = "Password"
                    HIGHLIGHT = SELECTED = [False, "n"]
            # if any textbox selected and key typed
            if SELECTED[0] == True:
                if event.type == KEYDOWN:
                    if SELECTED[1] == "u":
                        cText = text
                    elif SELECTED[1] == "p":
                        cText = password
                    if event.key == TAB:  # Switch from username to password with Tab
                        if SELECTED[1] == "u":
                            SELECTED[1] = "p"
                            text = cText
                            if text == "":
                                text = "Username"
                            if password == "Password":
                                password = ""
                            pygame.display.update()
                            continue
                        elif SELECTED[1] == "p":
                            SELECTED[1] = "u"
                            password = cText
                            if password == "":
                                password = "Password"
                            if text == "Username":
                                text = ""
                            pygame.display.update()
                            continue
                    elif event.key in SHIFT + CTRL + ALT:
                        cText = cText  # Makes no change
                    elif event.key == K_BACKSPACE:
                        cText = cText[:-1]  # Show all letters except the last one
                    elif event.key == K_SPACE:
                        cText = cText  # Makes no change
                    elif event.key == ENTER:
                        SELECTED = HIGHLIGHT = [False, "n"]
                    else:
                        cText += chr(event.key)
                    if len(cText) > 18:  # if the textbox has reached the max word limit of 18 words
                        continue
                    if SELECTED[1] == "u":
                        text = cText
                    elif SELECTED[1] == "p":
                        password = cText
        # highlighting the username and password textboxes
        if HIGHLIGHT[0] == True:
            if HIGHLIGHT[1] == "u":
                highlight(username, BLUE)
            if HIGHLIGHT[1] == "p":
                highlight(passRect, BLUE)
        if SELECTED[0] == True:
            if SELECTED[1] == "u":
                highlight(username, BLUE)
            if SELECTED[1] == "p":
                highlight(passRect, BLUE)
        pygame.display.update()

def encryptUsername(word):  # Encrypts word to store them safely
    eWord = ""  # holds encrypted word
    for i in word:
        # convert each alphabet into a 3 digit number
        if ord(i) < 100:  # if the length of ord(i) is 2 i.e ord("a") == 98
            eWord += "0%s" % str(ord(i))
        else:           # eg ord("f") == 102
            eWord += str(ord(i))
    return eWord

def hashPass(password):  # generates a single digit from a password
    ePass = 0  #encrypted password
    for i in password:
        ePass += ord(i)
    ePass = str(ePass)
    while len(ePass) != 1:
        ePass1 = 0  # temporarily store digits of ePass
        for i in ePass:
            ePass1 += int(i)
        ePass = str(ePass1)
    return ePass

def validatePassOrder(password):  # Created this function because the user was able to log in with the password "cba" even when the true password was "abc".
    # This function checks if the order of words in a password is correct.
    ePass = ""
    for i in password:
        j = list(str(ord(i)))  # Turns ord(i) into string and makes its list.
        j.reverse()  # Reverses it so that we can get its last digit at first place.
        ePass += j[0]  # stores the first digit (last digit in the actual) of ord(i)
    return ePass

def userNum():  # Shows current number of accounts in the system
    with open("Data/userData.txt") as file:
        data = file.readlines()
        return (len(data))

def homepage(musicPlaying, startupCheck):  # Starting page with Sign Up, Log In and Exit options
    HIGHLIGHT = [False, "n"]
    if startupCheck:
        startupCheck = False        # Make sure this checking occur only once when the program starts at first
        # Checking if the word list and their score files are fine
        errorDetected = False
        try:
            if (not os.path.isfile("Data/mScore.txt") or not os.path.isfile("Data/sScore.txt") or not os.path.isfile("Data/aScore.txt")):
                errorDetected = True
            else:
                mScore, sScore, aScore = getScore("Meaning"), getScore("Synonym"), getScore("Antonym")
                tempMscore = []
                tempSscore = []
                tempAscore = []
                for x in range(len(mScore)):
                    tempMscore.append("".join(mScore[x][1:]))
                    tempSscore.append("".join(sScore[x][1:]))
                    tempAscore.append("".join(aScore[x][1:]))
                mode = ["Meaning", "Synonym", "Antonym"]
                score = [tempMscore, tempSscore, tempAscore]
                for i in range(3):
                    progressBar(2, "Checking %s out of 3. ." % (i+1))
                    word = getWordList(mode[i])
                    for j in range(len(score[i])):
                        if len(score[i][j]) != len(getWordList(mode[i])) and len(score[i]) != 0:
                            errorDetected = True
        except:
            errorDetected = True
        if errorDetected:
            progressBar(1, "Error Detected!")
            progressBar(1, "Repairing the error. . .")
            progressBar(1, "Resetting the program. . .")
            progressBar(1, "Clearing user data and scores. . .")
            import ResetProgram
    if userNum() == 0:
        signUp(musicPlaying, startupCheck)
    while True:
        users = str(userNum())
        windowSurface.fill(BLACK)
        makeLogo()
        musicLogo(musicPlaying, musicRect)
        writeText("Users in the database:", WHITE, pygame.Rect(WINW - 190, logoRect.top, 0, 0), 15, False)
        writeText(users, BLUE, pygame.Rect(WINW - 105, logoRect.top + 20, 0, 0), 24, False)
        SignUp = button("Sign Up", HIGHLIGHT, pygame.Rect(170, logoRect.bottom, 50, 25), [True, "s"])
        LogIn = button("Log In", HIGHLIGHT, pygame.Rect(SignUp.right + 10, logoRect.bottom, 50, 25), [True, "l"])
        Quit = button("Quit", HIGHLIGHT, pygame.Rect(LogIn.right + 10, logoRect.bottom, 50, 25), [True, "q"])
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                x, y = event.pos
                if SignUp.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                elif LogIn.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "l"]
                elif Quit.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "q"]
                else:
                    HIGHLIGHT = [False, "n"]
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if SignUp.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                    buttonClickAnimation(pygame.Rect(170, logoRect.bottom, 50, 25), "Sign Up")
                    progressBar(2, "Loading Page. . .")
                    signUp(musicPlaying, startupCheck)
                elif LogIn.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "l"]
                    buttonClickAnimation(pygame.Rect(SignUp.right + 10, logoRect.bottom, 50, 25), "Log In")
                    progressBar(2, "Loading Page. . .")
                    logIn(musicPlaying, startupCheck)
                elif Quit.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "q"]
                    buttonClickAnimation(pygame.Rect(LogIn.right + 10, logoRect.bottom, 50, 25), "Quit")
                    pygame.quit()
                    sys.exit()
                elif musicRect.colliderect((x, y, 0, 0)):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                else:
                    HIGHLIGHT = [False, "n"]
        pygame.display.update()

def signUp(musicPlaying, startupCheck):  # Sign up page
    userName = "Username"
    password = "Password"
    HIGHLIGHT = SELECTED = [False, "n"]
    board(userName, password, HIGHLIGHT, SELECTED, "Sign up", musicPlaying, startupCheck)

def logIn(musicPlaying, startupCheck):  # Log in page
    global userName
    userName = "Username"
    password = "Password"
    HIGHLIGHT = SELECTED = [False, "n"]
    userName, musicPlaying = board(userName, password, HIGHLIGHT, SELECTED, "Log in", musicPlaying, startupCheck)
    home(userName, musicPlaying, startupCheck)

def musicLogo(musicPlaying, musicRect):  # Draws the music logo according to its current status
    musicLayout = pygame.image.load("Data/layout.png")
    sMusicLayout = pygame.transform.scale(musicLayout, (musicRect.width + 20, musicRect.height + 20))
    windowSurface.blit(sMusicLayout, pygame.Rect(musicRect.left - 8, musicRect.top - 10, musicRect.width + 5, musicRect.height + 5))
    if musicPlaying == True:
        musicLogo = pygame.image.load("Data/musicOn.png")
        sMusicLogo = pygame.transform.scale(musicLogo, (musicRect.width, musicRect.height))
    elif musicPlaying == False:
        musicLogo = pygame.image.load("Data/musicOff.png")
        sMusicLogo = pygame.transform.scale(musicLogo, (musicRect.width, musicRect.height))
    windowSurface.blit(sMusicLogo, musicRect)

def buttonClickAnimation(rect, text):  # When the buttons are clicked, they will move out of the window
    y = int(2 * WINH / 3)
    while rect.centery != y:
        if rect.centery < y:
            rect.centery += 1
        elif rect.centery > y:
            rect.centery -= 1
        tempButton = button(text, False, rect, [True, "t"])  # tempButton holds the rect data of currently clicked rectangle and also draws it on surface
        pygame.display.update()
    for n in range(0, 200):
        while rect.left < WINW + 10:
            rect.left += n  # The value of n increases such that the button accelerates
            tempButton = button(text, False, rect, [True, "t"])
            pygame.display.update()
            mainClock.tick(25)
            break
        if rect.left > WINW + 10:  # When crosses the window
            break

def newUserScore(userName):  # Makes empty score for new users when they sign up
    for wordList, scoreText in [["wordList.txt", "mScore.txt"], ["synonym.txt", "sScore.txt"], ["wordList.txt", "aScore.txt"]]:
        with open("Data/"+wordList) as file:  # Open the word list
            data = file.readlines()
            score = "N" * len(data)  # Make "N" (Not Tried) for every word in the wordlist
            splitScore = [score[i:i + grpItems] for i in range(0, len(data), grpItems)]
            # Split the series of "NNNNNNNNNNNNNNNN. . . . . N" to "NNNNNNNNNN NNNNNN . . . . N" where each group is seperated by a space
            line = " ".join([userName]+splitScore)
            with open("Data/"+scoreText, "a") as scoreFile:  # Write the groups' scores
                scoreFile.write(line + "\n")

# Codes below are used after the user logs in his/her account

def home(userName, musicPlaying, startupCheck):  # Starting page after the user sign in
    HIGHLIGHT = [False, "n"]
    logout = False
    while True:
        windowSurface.fill(BLACK)
        musicLogo(musicPlaying, musicRect)
        font = pygame.font.SysFont("Comic Sans MS", 16, True)
        textObj = font.render(userName, True, WHITE)
        textRect = textObj.get_rect()
        textRect.right = WINW - 20
        textRect.top = 20
        userImage = pygame.image.load("Data/user.png")  # Load userLogo
        sImage = pygame.transform.scale(userImage, (textRect.width + 10, textRect.height + 6))
        windowSurface.blit(sImage, textRect)  # Makes userLogo on the screen
        # Align userName inside userLogo
        textRect.topleft = (textRect.left+5, textRect.top+3)
        windowSurface.blit(textObj, textRect)  # Writes userName on the userLogo on the screen
        makeLogo()
        practice = button("Practice", HIGHLIGHT, pygame.Rect(logoRect.left - 10, logoRect.bottom + 10, 50, 25), [True, "p"])
        score = button("Score", HIGHLIGHT, pygame.Rect(practice.right + 10, logoRect.bottom + 10, 50, 25), [True, "s"])
        logOut = button("Log Out", HIGHLIGHT, pygame.Rect(score.right + 10, logoRect.bottom + 10, 50, 25), [True, "l"])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                x, y = event.pos
                if practice.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "p"]
                elif score.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                elif logOut.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "l"]
                else:
                    HIGHLIGHT = [False, "n"]
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if practice.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "p"]
                    buttonClickAnimation(pygame.Rect(logoRect.left - 10, logoRect.bottom + 10, 50, 25), "Practice")
                    selectMode(userName, HIGHLIGHT, musicPlaying, startupCheck)
                elif score.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                    buttonClickAnimation(pygame.Rect(practice.right + 10, logoRect.bottom + 10, 50, 25), "Score")
                    scoreBoard(userName, HIGHLIGHT, musicPlaying, startupCheck)
                elif logOut.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "l"]
                    buttonClickAnimation(pygame.Rect(score.right + 10, logoRect.bottom + 10, 50, 25), "Log Out")
                    logout = True
                elif musicRect.colliderect((x, y, 0, 0)):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                else:
                    HIGHLIGHT = [False, "n"]
        if logout:  # If logout button clicked and logout == True
            progressBar(2, "Signing out. . .")
            homepage(musicPlaying, startupCheck)
        pygame.display.update()

def getWordList(mode):  # Retrives wordlist for given mode i.e meaning, antonym or synonym and returns it as list
    textFile = {"Meaning" : "wordList.txt", "Synonym":"synonym.txt", "Antonym":"wordList.txt"}
    wordList = []
    with open("data/"+textFile[mode]) as file:
        data = file.readlines()
        for line in data:
            if mode == "Synonym":  # For synonym mode
                wordList.append(line.split())
            else:  # For meaning and antonym mode.
                # Same wordlist for meaning and antonym as they both are in the same wordlist
                wordList.append(line.split(":"))  # splits the line at only once in space and divides it into two items i.e word and meaning
        return wordList

def groupWords(wordList, grpItems):  # Convert the list of words ['cat', 'dog', 'bat', 'horse'] in wordList into list of lists of words [['cat', 'dog'] , ['bat', 'horse']] where each sub-list represent a group
    NUM = len(wordList)  # Total number of words
    # Determines the number of groups needed to store all the words from a wordlist
    if 0 < (NUM % grpItems) <= (grpItems / 2):  # If remainder is half the grpItems i.e if grpItems = 10 and NUM = 14, this condition will be 0 < 14/10 < 5
        GNUM = round(NUM / grpItems) + 1  # Adds one as round(14/10) = 1 but we will need one extra group to store the remaining 4 words
    elif (NUM % grpItems) > (grpItems / 2):  # remainder above the grpItems
        GNUM = round(NUM / grpItems)  # round(16/10) = 2. So there will be 10 words in one group and 6 in another
    else:  #No remainder
        GNUM = round(NUM / grpItems)
    # Grouping process starts now using the GNUM obtained above
    groups = [wordList[i:i + grpItems] for i in range(0, NUM, grpItems)] # Slice items to groups of 'grpItems' items in it
    return groups

def askQuestion(group, grpNum, score, mode, musicPlaying, HIGHLIGHT, startupCheck):   # Displays the word on the screen with 4 answers choices
    helps = 5
    for i in range(len(group[grpNum])):
        ANSWERRECTS = [pygame.Rect(50, 160, 400, 25), pygame.Rect(50, 190, 400, 25), pygame.Rect(50, 220, 400, 25), pygame.Rect(50, 250, 400, 25)]       # Rectangle values for answer choices
        if helps == 0:
            helpUsed = True
        else:
            helpUsed = False
        answerChoosed = False
        questionChoosed = False
        wAns = "A B C D".split()
        ans2remove = "#"             # Stores the option to be removed when the help feature used
        oldSelectedAns = []         #  Stores the 4 answer choices until the current word gets a response
        while not answerChoosed:
            windowSurface.fill(BLACK)
            skipRect = skip()
            musicLogo(musicPlaying, musicRect)
            if mode == "Meaning":
                word, meaning = group[grpNum][i][0], group[grpNum][i][1]
            elif mode == "Synonym":
                if not questionChoosed:
                    x, y = 0, 0     # x and y will be used as index for word and meaning
                    while x == y:       # Loop while x and y have same integer values because we don't want have its question word and one answer choice same
                        x = random.randint(0, len(group[grpNum][i])-1)
                        y = random.randint(0, len(group[grpNum][i])-1)
                    questionChoosed = True
                    word, meaning = group[grpNum][i][x].strip("\n"), group[grpNum][i][y].strip("\n")
            elif mode == "Antonym":           # Antonym
                word, meaning = group[grpNum][i][0], group[grpNum][i][2].strip("\n")
            # Codes for toolbar containing helps left, question status and current question number out of total
            qStatus = status(userName, grpNum, i, score)            # Holds the status of current question
            statusColor = {"Correct" : GREEN, "Wrong" : RED, "Skipped" : YELLOW, "Not Done Yet" : SILVER}       # Dic with color for different question status
            hText = writeText("Helps left: ", WHITE, pygame.Rect(musicRect.left-10, musicRect.bottom+10, 15, 10), 14, True)
            # Help options needed here
            sText = writeText("Status: ", WHITE, pygame.Rect(230, musicRect.bottom+10, 18, 10), 14, True)
            writeText(qStatus, statusColor[qStatus], pygame.Rect(sText.right+5, musicRect.bottom+10, 25, 10), 14, False)
            qText = writeText("of", WHITE, pygame.Rect(WINW-50, musicRect.bottom+10, 8, 10), 14, True)
            if len(str(i+1)) == 1:
                writeText(str(i+1), BLUE, pygame.Rect(qText.left-15, qText.top-5, 10, 10), 20, False)
            elif len(str(i+1)) == 2:
                writeText(str(i+1), BLUE, pygame.Rect(qText.left-25, qText.top-5, 10, 10), 20, False)
            writeText(str(len(group[grpNum])), WHITE, pygame.Rect(qText.right+5, musicRect.bottom+10, 10, 10), 14, False)
            helpRect = help(hText, helpUsed, helps)
            # Codes for current word asked and the four answer choices for it
            writeText(word.capitalize(), SILVER, pygame.Rect((WINW/2)-40, musicRect.bottom+50, 50, 15), 24, False)
            cAns, oldSelectedAns = generateAnswers(meaning, group, grpNum, ans2remove, oldSelectedAns, mode, ANSWERRECTS)         # writes the four answer choices on the screen and return correct ans and oldList of answers
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION:
                    x, y = event.pos
                    for rect in ANSWERRECTS:
                        if rect.colliderect((x, y, 0, 0)):
                            HIGHLIGHT = [True, "r"]
                            break
                        else:
                            HIGHLIGHT = [False, "n"]
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for rect in ANSWERRECTS:
                        if rect.colliderect((x, y, 0, 0)):
                            answerChoosed = True
                            HIGHLIGHT = [True, "r"]
                            rectIndex = ANSWERRECTS.index(rect)
                            answer = chr(ord("A")+rectIndex)
                            if answer == cAns:          # If correct
                                updateScore(userName, score, mode, grpNum, i, "C")
                                checkAnswer(True)
                            else:
                                updateScore(userName, score, mode, grpNum, i, "W")
                                rect = ANSWERRECTS[ord(cAns)-ord("A")]
                                highlight(pygame.Rect(rect.left-25, rect.top, rect.width, rect.height), GREEN)
                                checkAnswer(False)
                            break
                    if musicRect.colliderect((x, y, 0, 0)):
                        if musicPlaying:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1, 0.0)
                        musicPlaying = not musicPlaying
                    elif helpRect.colliderect((x, y, 0, 0)):
                        if not helpUsed:
                            helpUsed = True
                            wAns.remove(cAns)   # remove correct answer from the answer choices
                            ans2remove = random.choice(wAns)
                            helps -= 1      # reduce help count
                    elif skipRect.colliderect((x, y, 0, 0)):
                        updateScore(userName, score, mode, grpNum, i, "S")
                        answerChoosed = True
                    else:
                        HIGHLIGHT = [False, "n"]
            if HIGHLIGHT[0]:
                if HIGHLIGHT[1] == "r":
                    highlight(pygame.Rect(rect.left-25, rect.top, rect.width, rect.height), RED)
            pygame.display.update()
            pygame.event.clear()        # remove any previous clicks or events before asking another question
    progressBar(2, "Calculating test performance. . .")
    showTestResult(userName, score, grpNum, HIGHLIGHT, musicPlaying, startupCheck)

def checkAnswer(correct):
    if correct == True:     # If correct
        sign = pygame.transform.scale(pygame.image.load("Data/correct.png"), (100, 100))
    else:
        sign = pygame.transform.scale(pygame.image.load("Data/wrong.png"), (100, 100))
    signRect = pygame.Rect(0, WINH-250, 100, 100)
    signRect.centerx = windowSurface.get_rect().centerx
    windowSurface.blit(sign, signRect)
    pygame.display.update()
    time.sleep(1)

def skip():         # draw a skip button
    skipButton = pygame.Rect(WINW-100, 150, 100, 200)
    skipImg = pygame.transform.scale(pygame.image.load("Data/skip.png"), (100, 200))
    windowSurface.blit(skipImg, skipButton)
    return skipButton

def help(rect, helpChoosed, helps):         # draw a help button
    # help left status
    helpIconRects = []
    for x in range(helps):      # draws helps icons equal to helps left
        helpIconRects.append(pygame.Rect(rect.right + x*15, rect.top+4, 15, 15))
        helpIcon = pygame.transform.scale(pygame.image.load("Data/help_icon.png"), (15, 15))
        windowSurface.blit(helpIcon, helpIconRects[-1])
    # Help button
    helpButton = pygame.Rect(0, WINH-100, 200, 100)
    helpButton.centerx = windowSurface.get_rect().centerx
    if not helpChoosed:
        helpImg = pygame.transform.scale(pygame.image.load("Data/help_on.png"), (200, 100))
    elif helpChoosed:
        helpImg = pygame.transform.scale(pygame.image.load("Data/help_off.png"), (200, 100))
    windowSurface.blit(helpImg, helpButton)
    return helpButton

def generateAnswers(meaning, group, grpNum, remove, oldList, mode, ANSWERRECTS):    # Generates 4 answer choices and returns position of correct answer
    # I used oldList to keep track of old list of answers used before help was asked and make sure the order of new answers don't change.
    if oldList == []:
        selectedAns = [meaning]         # stores the 4 answers to be shown. Correct answer already added
        while True:
            x = random.choice(group[grpNum])        # randomly selects a word and meaning of the same group
            if mode == "Meaning":
                if x[1] not in selectedAns:
                    selectedAns.append(x[1])
            if mode == "Synonym":
                i = random.randint(0, len(x)-1)
                if x[i].strip("\n") not in selectedAns and meaning not in x:
                    selectedAns.append(x[i].strip("\n"))
            if mode == "Antonym":
                if x[2].strip("\n") not in selectedAns:
                    selectedAns.append(x[2].strip("\n"))            # Have to strip the string to remove "\n" from the answers
            if len(selectedAns) == 4:                       # When four options created
                random.shuffle(selectedAns)             # Shuffle the answers in the list
                break
        oldList = selectedAns
    # Display the answer choices
    for j in range(len(oldList)):
        tempRect = ANSWERRECTS[j]
        if meaning == oldList[j]:
            correctAns = chr(ord("A")+j)
        writeText((chr(ord("A")+j)+")"), WHITE, pygame.Rect(tempRect.left-20, tempRect.top, 0, 0) , 16, False)      # Write A, B, C or D ahead of answer choices
        if chr(ord("A") + j) == remove:         # If skips one wrong option as requested by help
            writeText("", WHITE, tempRect, 0, False)  # display a blank line if help asked
            tempRect.width = 0                # Changes the width of blank rect to 0
            continue
        writeText(oldList[j], WHITE, tempRect, 16, False)             # write the answer choice
    return correctAns, oldList

def updateScore(userName, score, mode, grpNum, qNum, value):     # updates mScore/sScore/aScore and writes them to respective txt file
    for x in score:
        if x[0] != userName:
            continue    # move to another list until we get the score list of current user
        # When the score list of current user is reached
        groupL = list(x[grpNum+1])            # temporarily stores the score of a group
        groupL[qNum] = value            # here value = "C" for correct and "W" for wrong and "N" for not done
        groupL = "".join(groupL)        # Thanks Aritra for the idea :)
        x[grpNum+1] = groupL
        if mode == "Meaning":
            with open("Data/mScore.txt", "w") as file:
                for a in score:
                    for b in a:
                        file.write(b+" ")
                    file.write("\n")        # breaks line
        elif mode == "Synonym":
            with open("Data/sScore.txt", "w") as file:
                for a in score:
                    for b in a:
                        file.write(b+" ")
                    file.write("\n")
        elif mode == "Antonym":
            with open("Data/aScore.txt", "w") as file:
                for a in score:
                    for b in a:
                        file.write(b+" ")
                    file.write("\n")

def showTestResult(userName, score, grpNum, HIGHLIGHT, musicPlaying, startupCheck):        # Shows the result after the test taken
    while True:
        windowSurface.fill(BLACK)
        musicLogo(musicPlaying, musicRect)
        close = button("Close", HIGHLIGHT, pygame.Rect(WINW-70, 0, 20, 10), [True, "c"])
        for i in score:
            correct, total = 0, 0
            if i[0] != userName:
                continue
            titleRect = pygame.Rect(0, musicRect.bottom+5, 280, 20)
            titleRect.centerx = windowSurface.get_rect().centerx
            titleRect = writeText("Your performance report:", WHITE, titleRect, 24, True)
            pygame.draw.rect(windowSurface, SILVER, (titleRect.left - 3, titleRect.top -2, titleRect.width+6, titleRect.height+4), 2)
            tempRect = []
            for j in range(len(i[grpNum+1])):
                if j+1 <= grpItems/2:
                    tempRect.append(pygame.Rect( 60 , titleRect.bottom + 20 + j*25, 60, 15))
                else:
                    tempRect.append(pygame.Rect( 200 , titleRect.bottom + 20 + (j-5)*25, 60, 15))
                if i[grpNum+1][j] == "C": # correct
                    writeText("%s) Correct" % (j+1), GREEN, tempRect[-1], 16, False)
                    correct += 1
                    total += 1
                if i[grpNum+1][j] == "W": # Wrong
                    writeText("%s) Wrong" % (j+1), RED, tempRect[-1], 16, False)
                    total += 1
                if i[grpNum+1][j] == "N": # not done yet
                    writeText("%s) Not Done" % (j+1), SILVER, tempRect[-1], 16, False)
                if i[grpNum+1][j] == "S": # skipped
                    writeText("%s) Skipped" % (j+1), YELLOW, tempRect[-1], 16, False)
            tempRect = tempRect[-1]     # Reusing the same varible for storing just the last rectangle coordinates as other coordinates are not needed now
            tempRect.top += 40
            if total == 0:
                tempRect.width = 470
                tempRect.centerx = windowSurface.get_rect().centerx
                resultRect = writeText("No result as you skipped all questions.", RED, tempRect, 24, True)
                pygame.draw.rect(windowSurface, SILVER, (resultRect.left - 3, resultRect.top -2, resultRect.width+6, resultRect.height+4), 2)
            if total != 0:
                tempRect.width = 180
                tempRect.centerx = windowSurface.get_rect().centerx
                resultRect = writeText(str(correct)+" correct out of "+str(total), WHITE, tempRect, 24, True)
                pygame.draw.rect(windowSurface, SILVER, (resultRect.left - 3, resultRect.top -2, resultRect.width+6, resultRect.height+4), 2)
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                x, y = event.pos
                if close.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "c"]
                else:
                    HIGHLIGHT = [False, "n"]
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if musicRect.colliderect((x, y, 0, 0)):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                elif close.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "c"]
                    home(userName, musicPlaying, startupCheck)
        pygame.display.update()

def getScore(mode):         # Reads the score files (mScore, sScore & aScore) and returns them as lists
    scoreFile = {"Meaning" : "mScore.txt", "Synonym" : "sScore.txt", "Antonym" : "aScore.txt"}
    with open("Data/"+scoreFile[mode]) as file:
        score = []             # Score for current mode
        data = file.readlines()
        for line in data:
            score.append(line.split())
    return score

def status(userName, grpNum, qNum, score):  # checks if a question was answered or skipped and, if answered, was it correct or wrong.
    for items in score:
        if userName == items[0]:        # if list of current user
            for x in items[grpNum+1]:
                if items[grpNum+1][qNum] == "C":
                    return "Correct"
                if items[grpNum+1][qNum] == "W":
                    return "Wrong"
                if items[grpNum+1][qNum] == "N":
                    return "Not Done Yet"
                if items[grpNum+1][qNum] == "S":
                    return "Skipped"

def selectMode(userName, HIGHLIGHT, musicPlaying, startupCheck):
    showGroups = False
    mode = ""
    while True:
        windowSurface.fill(BLACK)
        musicLogo(musicPlaying, musicRect)
        back = button("Back", HIGHLIGHT, pygame.Rect(WINW-60, 0, 20, 10), [True, "b"])
        makeLogo()
        text = writeText("Select Mode:", WHITE, pygame.Rect(20, logoRect.bottom+35, 25, 10), 20, True)
        meaning = button("Meaning", HIGHLIGHT, pygame.Rect(text.right+10, logoRect.bottom + 10, 50, 15), [True, "m"])
        synonym = button("Synonym", HIGHLIGHT, pygame.Rect(meaning.right + 10, logoRect.bottom + 10, 50, 15), [True, "s"])
        antonym = button("Antonym", HIGHLIGHT, pygame.Rect(synonym.right + 10, logoRect.bottom + 10, 50, 15), [True, "a"])
        groupRects = []     # Stores the rectangle value of groups
        if showGroups:      # When one mode is clicked and showGoups == True
            groupText = writeText("Select Group:", WHITE, pygame.Rect(20, logoRect.bottom+70, 25, 15), 20, True)
            x = 0           # Keeps track of how many time the lines changed while arrangeing all the groups on the screen
            tempGrpRect = pygame.Rect(groupText.right+10, logoRect.bottom+70, 65, 25)       # Temporarily holds the rectangle coordinates of the current group rectangle. Initial value assigned
            for i in range(len(group)):     # generates and stores the coordinates of rectangles of the groups
                if (i+1)%5 == 0 and i != 0:
                    x += 1
                if (i+1)%5 == 1:
                    tempGrpRect = pygame.Rect(groupText.right+10, logoRect.bottom+75+x*30, 65, 25)
                groupRects.append(pygame.Rect(tempGrpRect.left, tempGrpRect.top, tempGrpRect.width, tempGrpRect.height))
                tempGrpRect.left = tempGrpRect.right + 5
            for i in range(len(groupRects)):
                tempGrpRect = groupRects[i]     # The variable is reused to temporarily hold the value of coordinates of current rectangle.
                writeText("Group %s"%(i+1), WHITE, tempGrpRect, 15, False)
                pygame.draw.rect(windowSurface, WHITE, (tempGrpRect.left-5, tempGrpRect.top-2, tempGrpRect.width, tempGrpRect.height), 2)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                x, y = event.pos
                if back.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "b"]
                elif meaning.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "m"]
                elif synonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                elif antonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "a"]
                else:
                    HIGHLIGHT = [False, "n"]
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if musicRect.colliderect((x, y, 0, 0)):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                elif back.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "b"]
                    home(userName, musicPlaying, startupCheck)
                elif meaning.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "m"]
                    mode = "Meaning"
                    showGroups = True
                    wordList = getWordList(mode)   # Gets the wordlist for meaning mode
                    group = groupWords(wordList, grpItems)      # Groups the words in the wordList with each group having number of items equal to grpItems
                    score = getScore(mode)
                elif synonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                    mode = "Synonym"
                    showGroups = True
                    wordList = getWordList(mode)
                    group = groupWords(wordList, grpItems)
                    score = getScore(mode)
                elif antonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "a"]
                    mode = "Antonym"
                    showGroups = True
                    wordList = getWordList(mode)
                    group = groupWords(wordList, grpItems)
                    score = getScore(mode)
                else:
                    HIGHLIGHT = [False, "n"]
                    showGroups = False
                # if clicked over a group
                for i in range(len(groupRects)):
                    if groupRects[i].colliderect((x, y, 0, 0)):
                        grpNum = i
                        askQuestion(group, grpNum, score, mode, musicPlaying, HIGHLIGHT, startupCheck)
        pygame.display.update()

def scoreBoard(userName, HIGHLIGHT, musicPlaying, startupCheck):  # Prints all users' scores for a chosen mode
    scoreChoosed = False
    while not scoreChoosed:
        windowSurface.fill(BLACK)
        musicLogo(musicPlaying, musicRect)
        back = button("Back", HIGHLIGHT, pygame.Rect(WINW-60, 0, 20, 10), [True, "b"])
        makeLogo()
        meaning = button("Meaning Score", HIGHLIGHT, pygame.Rect(20, logoRect.bottom + 10, 80, 15), [True, "m"])
        synonym = button("Synonym Score", HIGHLIGHT, pygame.Rect(meaning.right + 8, logoRect.bottom + 10, 80, 15), [True, "s"])
        antonym = button("Antonym Score", HIGHLIGHT, pygame.Rect(synonym.right + 8, logoRect.bottom + 10, 80, 15), [True, "a"])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                x, y = event.pos
                if back.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "b"]
                elif meaning.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "m"]
                elif synonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                elif antonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "a"]
                else:
                    HIGHLIGHT = [False, "n"]
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if musicRect.colliderect((x, y, 0, 0)):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                elif back.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "b"]
                    home(userName, musicPlaying, startupCheck)
                elif meaning.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "m"]
                    score = "mScore.txt"
                    scoreChoosed = True
                    buttonClickAnimation(pygame.Rect(20, logoRect.bottom + 10, 80, 15), "Meaning Score")
                elif synonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "s"]
                    score = "sScore.txt"
                    scoreChoosed = True
                    buttonClickAnimation(pygame.Rect(meaning.right + 8, logoRect.bottom + 10, 80, 15), "Synonym Score")
                elif antonym.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "a"]
                    score = "aScore.txt"
                    scoreChoosed = True
                    buttonClickAnimation(pygame.Rect(synonym.right + 8, logoRect.bottom + 10, 80, 15), "Antonym Score")
                else:
                    HIGHLIGHT = [False, "n"]
        pygame.display.update()
    while True:
        windowSurface.fill(BLACK)
        musicLogo(musicPlaying, musicRect)
        back = button("Back", HIGHLIGHT, pygame.Rect(WINW-60, 2, 20, 10), [True, "b"])
        if score == "mScore.txt":
            modeScore = writeText("Meaning Score:", BLUE, pygame.Rect(20, back.bottom + 10, 50, 50), 18, True)  # Writes the text and stores coordinates of its rectangle
        elif score == "sScore.txt":
            modeScore = writeText("Synonym Score:", BLUE, pygame.Rect(20, back.bottom + 10, 50, 50), 18, True)
        elif score == "aScore.txt":
            modeScore = writeText("Antonym Score:", BLUE, pygame.Rect(20, back.bottom + 10, 50, 50), 18, True)
        title = writeText("Username                 Answer Accuracy (%)", GREEN, pygame.Rect(20, modeScore.bottom + 5, 50, 50), 15, True)
        with open("Data/"+score) as file:
            tempScore = pygame.Rect(20, title.bottom + 10, 200, 25)
            data = file.readlines()
            for line in data:
                line = line.split()
                user = line[0]
                line.remove(user)  # removes the user name from the list so that only scores remain
                line = "".join(line)  # Converts list to string
                correct = line.count("C")  # Count correct answers & thanks Aritra for the idea :)
                total = correct + line.count("W")  # Count total answers
                if total == 0:
                    writeText(user, WHITE, tempScore, 14, False)
                    writeText("Not practiced yet.", RED, pygame.Rect(tempScore.left + 200, tempScore.top, tempScore.width, tempScore.height), 14, False)
                else:
                    writeText(user, WHITE, tempScore, 14, False)
                    writeText(str(round((100 * correct / total), 2)) + " %", WHITE, pygame.Rect(tempScore.left + 250, tempScore.top, tempScore.width, tempScore.height), 14, False)
                tempScore.top += 20
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                x, y = event.pos
                if back.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "b"]
                else:
                    HIGHLIGHT = [False, "n"]
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if musicRect.colliderect((x, y, 0, 0)):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                elif back.colliderect((x, y, 0, 0)):
                    HIGHLIGHT = [True, "b"]
                    scoreBoard(userName, HIGHLIGHT, musicPlaying, startupCheck)
                else:
                    HIGHLIGHT = [False, "n"]
        pygame.display.update()
