import os
try:
        import PyDictionary
except:
        print("Please install PyDictionary Module.")
        print("Type 'pip install pydictionary' in command prompt")
        input("Module not found: PyDictionary Module not installed.")

def end():
        return input("Do you want to close the program? (y/n)").lower().startswith("y")

def main():
        print()
        print("This program creates wordlist by adding meanings, antonyms or synonyms in your wordlist.")
        print()
        print("Make sure your wordlist is in .txt format and each word is in seperate line.")
        print()
        listName = ""
        while True:
                while not os.path.isfile("{}.txt".format(listName)):
                        listName = input("Enter the name of the file with your words: ")
                        if not os.path.isfile("{}.txt".format(listName)):
                                print("File name {}.txt not found.".format(listName))
                                print()
                listName = listName+".txt"              # permanently add the .txt extension in the file name
                data = readFile(listName)
                print("File Loaded: {}".format(listName))
                print()
                print("Create: \n1) Meanings Only    2) Antonyms Only    3) Both Meaning and Antonym    4) Synonym Only")
                mode = 0
                while mode not in [1, 2, 3, 4]:
                        mode = int(input("Select: "))
                        if mode not in [1, 2, 3, 4]:
                                print("Option not available!")
                                print()
                if mode in [1, 3]:
                        data = downloadWords("mean", data)
                        if mode == 1:
                                writeWords("mean", data)
                if mode in [2, 3]:
                        data = downloadWords("anto", data)
                        writeWords("anto", data)
                if mode == 4:
                        data = downloadWords("syno", data)
                        writeWords("syno", data)
                if end:
                        return # get out of this function and end the program

def readFile(name):
        with open(name) as file:
                data = file.readlines()
                return [line.strip("\n").split(":") for line in data]

def downloadWords(mode, data):
        pd = PyDictionary.PyDictionary()
        if mode in ["anto", "mean"]:
                for item in data[:]:
                        try:
                                os.system("cls")
                                print("Progress: {} out of {} words{}".format(data.index(item)+1, len(data), ". "*((data.index(item)+1)%20)))
                                if mode == "anto":
                                        word = pd.antonym(item[0])
                                elif mode == "mean":
                                        word = pd.meaning(item[0])
                                # if the word has more than one meaning/antonym
                                if len(word) > 1:
                                        word = ", ".join(word)
                                # if the word has only one meaning/antonym
                                elif len(word) == 1:
                                        anto = anto[0]
                                data[data.index(item)].append(word)           
                        except:
                                if mode == "anto":              # if error occurs in antonym mode
                                      print("Antonym for {} wasn't found!".format(item[0]))
                                else:                                   # if error occurs in meaning mode
                                      print("Meaning for {} wasn't found!".format(item[0]))
                return data
        elif mode == "syno":
                SYNONYMS = []
                for item in data:
                        try:
                                os.system("cls")
                                print("Progress: {} out of {} words{}".format(data.index(item)+1, len(data), ". "*((data.index(item)+1)%20)))
                                item = item[0].split()
                                syno = pd.synonym(item[0])
                                syno = " ".join([item[0]]+syno)
                                SYNONYMS.append(syno)
                        except:
                                pass
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
