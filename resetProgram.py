# Resets the program and erases all scores & user data
import time

print("Reseting the program. . .")
time.sleep(1)

with open("userData.txt", "w") as file:
    file.write("")
    print()
    print("  User Data erased!")
    print()
    time.sleep(1)

with open("mScore.txt", "w") as file:
    file.write("")

with open("sScore.txt", "w") as file:
    file.write("")

with open("aScore.txt", "w") as file:
    file.write("")
    print("  All scores erased!")
    print()
    time.sleep(1)


input("Press any key to exit ")
