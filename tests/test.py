print("stdout and stdin test")

while(True):

    userinput = input("What is your name? ")
    print(f"Hello {userinput}")

    if userinput == "break": break

print("Goodbye")