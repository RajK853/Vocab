import os
try:
        import PyDictionary
except:
        print(" Please install PyDictionary Module.")
        print(" Type 'pip install pydictionary' in command prompt")
        input(" Module not found: PyDictionary Module not installed.")

def end():
        print()
        return input(" Do you want to close the program? (y/n) ").lower().startswith("y")

def main():
        print()
        print(" This program creates wordlist by adding meanings, antonyms or synonyms in your  wordlist.")
        print()
        print(" Make sure your wordlist is in .txt format and each word is in seperate line.")
        listName = ""
        while True:
                while not os.path.isfile("{}.txt".format(listName)):
                        print()
                        listName = input(" Enter the name of the file with your words: ")
                        if not os.path.isfile("{}.txt".format(listName)):
                                print()
                                print(" File name {}.txt not found.".format(listName))
                                print()
                listName = listName+".txt"              # permanently add the .txt extension in the file name
                data = readFile(listName)
                print()
                print(" File Loaded: {}".format(listName))
                print()
                print(" Add: \n 1) Meanings Only    2) Antonyms Only    3) Both Meaning and Antonym\n 4) Synonym Only")
                modeNo = 0
                while modeNo not in [1, 2, 3, 4]:
                        modeNo = int(input(" Select: "))
                        if modeNo not in [1, 2, 3, 4]:
                                print(" Option not available!")
                                print()
                if modeNo in [1, 3]:
                        # remove any antonym or meaning from the word and keep the words only
                        data = [[word[0]] for word in data]
                        data = downloadWords("mean", data)
                        if modeNo == 1:
                                writeWords("mean", data)                          
                if modeNo in [2, 3]:
                        # remove any antonym already present in the word
                        data = [word[0:2] for word in data]
                        data = downloadWords("anto", data)
                        writeWords("anto", data)
                if modeNo == 4:
                        data = downloadWords("syno", data)
                        writeWords("syno", data)
                # display the files with their wordlist
                print()
                if modeNo == 4:
                        print(" Words are saved in 'synonyms.txt' file.")
                else:
                        print(" Words are saved in 'wordList.txt' file.")
                if end():
                        return # get out of this function and end the program
                os.system("cls")

def readFile(name):             # read the given word file and return its words as list of lists
        with open(name) as file:
                data = file.readlines()
                return [line.strip("\n").split(":") for line in data]

def downloadWords(mode, data):                  # download words accordingly to the mode selected
        pd = PyDictionary.PyDictionary()
        if mode in ["anto", "mean"]:
                if mode == "mean": text = "meanings"
                else: text = "antonyms"
                for item in data[:]:
                        try:
                                os.system("cls")
                                print()
                                print(" Downloading {}:".format(text))
                                print(" Progress: {} out of {} words{}".format(data.index(item)+1, len(data), ". "*((data.index(item)+1)%20)))
                                if mode == "anto":
                                        word = pd.antonym(item[0])
                                        # if the word has more than one antonym
                                        if len(word) > 1:
                                                word = ", ".join(word)
                                        # if the word has only one antonym
                                        elif len(word) == 1:
                                                word = word[0]
                                elif mode == "mean":
                                        word = pd.meaning(item[0])
                                        # word is returned as 'Abhor : verb \nregard with disgust and hatred.\n'
                                        # so the meaning is always between the two \n 
                                        word = word[word.index("\n")+1:-1]      # slicing between the two \n
                                data[data.index(item)].append(word)           
                        except:
                                if mode == "anto":              # if error occurs in antonym mode
                                        print(" Error while downloading antonym for {}!".format(item[0]))
                                else:                                   # if error occurs in meaning mode
                                        print(" Error while downloading meaning for {}!".format(item[0]))
                print(" All words downloaded.")
                return data
        elif mode == "syno":
                SYNONYMS = []
                for item in data:
                        try:
                                os.system("cls")
                                print()
                                print(" Downloading synonyms")
                                print(" Progress: {} out of {} words{}".format(data.index(item)+1, len(data), ". "*((data.index(item)+1)%20)))
                                item = item[0].split()
                                syno = pd.synonym(item[0])
                                syno = " ".join([item[0].lower()]+syno)
                                SYNONYMS.append(syno)
                        except:
                                print(" Error while downloading synonym for {}!".format(item[0]))
                print(" All words downloaded.")
                return SYNONYMS

def writeWords(mode, data):
        if mode in ["anto", "mean"]:
                with open("wordList.txt", "w") as file:
                        file.write("")  # make an empty file
                with open("wordList.txt", "a") as file:
                        for item in data:
                                line = ":".join(item)+"\n"
                                file.write(line)
        if mode == "syno":
                with open("synonyms.txt", "w") as file:
                        file.write("")
                with open("synonyms.txt", "a") as file:
                        for item in data:
                                file.write(item+"\n")

if __name__ == "__main__":
        main()
