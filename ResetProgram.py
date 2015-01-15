# Resets the program and erases all scores & user data
import time

print("Resetting the program. . .")
time.sleep(0.5)

with open("Data/userData.txt", "w") as file:
    file.write("")
    print()
    print("  User Data erased!")
    print()
    time.sleep(0.5)

with open("Data/mScore.txt", "w") as file:
    file.write("")

with open("Data/sScore.txt", "w") as file:
    file.write("")

with open("Data/aScore.txt", "w") as file:
    file.write("")
    print("  All scores erased!")
    print()
    time.sleep(0.5)


print("Resetting completed. . . .")
time.sleep(1)
