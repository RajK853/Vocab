# This program just shuffles the word list so that the words in each group get randomized.
# I recommend not to run this program.
# Run this program only if you want to randomize the list.

import random, time

for text in ["wordList.txt", "synomn.txt", "acronym.txt"]:
    with open(text, "r") as data:
        List = data.readlines()
        random.shuffle(List)
        with open(text, "w") as data:
            for line in List:
                data.write(line)
print("Word list shuffled!")
time.sleep(1)
print()
import resetProgram.py
