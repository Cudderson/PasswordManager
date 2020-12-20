# password manager current goals
# 2: authenticate user before giving them passwords

# long-term updates
# 1: encrypt password before sending it to file
# 2: create GUI for app

keys = {}  # dict to be read into from file


def AddPassword():
    print("Please enter a key for your new password. (ex. 'Instagram')\n")
    new_id = input("New Key: ")
    print("Please enter a password for new key: " + new_id)
    new_pass = input("New Password: ")
    new_pass2 = input("Enter your new password once again: ")
    if new_pass2 == new_pass:
        print("Ready to save new entry for " + new_id + " with password: " + new_pass)
        confirm_new_entry = input("If this is correct, type 'confirm'. (Type 'q' to quit): ")
        if confirm_new_entry == 'confirm':
            FileToDict()
            keys[new_id] = new_pass
            WriteDictToFile()
            print("New entry successful!!")
    elif new_pass2 == 'q':
        print("Quitting program")
        quit()
    else:
        print("New passwords did not match. No changes were made.")


def ViewPasswords():
    with open("my_passwords.txt", "r") as f:
        # "View all" block works
        key = input("Enter the ID of the password you need. (ex: 'twitter')\nOr, type 'all' to view all passwords: ")
        if key == "all":
            if input("View all passwords? Type confirm to continue: ") == "confirm":
                for line in f:
                    print(line),
        else:
            FileToDict()
            if key in keys:
                print("Your password for " + key + " is:\n" + keys[key])
            else:
                print("Yikes. Key: " + key + " does not exist.")
                print("Redirecting you to home page.")
                Introduction()
    End()


def ManagePasswords():
    print("Ready to manage passwords.")
    check = input("Press enter to continue. Otherwise, type 'q' to quit: ")
    FileToDict()
    if check != "q":
        change_pass = input("Enter the key of the password you'd like to change or remove. (ex. 'Twitter'): ")
        if change_pass in keys:
            print("Your current password for " + change_pass + " is: " + keys[change_pass])
            choice = input(
                "Press 'c' to change password for " + change_pass + ", or press 'r' to remove the key and password from file.")
            if choice == 'c':
                new_pass = input("Enter your new password for " + change_pass + ". Type 'q' to quit: ")
                if new_pass != 'q':
                    print("Changing password for " + change_pass + " from '" + keys[
                        change_pass] + "' to '" + new_pass + "'")
                    confirm_change = input("Type 'confirm' to continue. Or type 'q' to quit: ")
                    if confirm_change == 'confirm':
                        keys[change_pass] = new_pass
                        WriteDictToFile()
                        print("Password change successful!")
                    else:
                        print("Quitting program.")
                        quit()
                else:
                    print("Quitting Program.")
                    quit()
            elif choice == 'r':
                print("Ready to delete saved entry for " + change_pass + " with password " + keys[change_pass] + ".")
                confirm_removal = input(
                    "Type 'confirm' if you would like to delete this information forever. Type 'q' to quit: ")
                if confirm_removal == 'confirm':
                    keys.pop(change_pass)
                    WriteDictToFile()
                    print("Did it work?")
            elif choice == 'q':
                print("Okay. Quitting program now.")
                quit()
        else:
            print("I couldn't find key with name " + change_pass + ". Quitting program now.")
            quit()
    else:
        print("I did not understand that. Quitting program.")
        quit()
    End()


def FileToDict():
    keys.clear()
    with open("my_passwords.txt", "r") as f:  # this block opens file, then writes into dictionary, closes when done
        for line in f:
            x = (line.split())
            keys[x[0]] = x[1]


def WriteDictToFile():
    with open("my_passwords.txt", "w") as f:
        for x, y in keys.items():
            f.write(x + " " + y + "\n")


def Introduction():
    print("Welcome to your Password Manager. What would you like to do?")

    print('v - View Passwords\n'
          'a - Add Password\n'
          'm - Manage Passwords\n'
          'q - Quit program\n')

    mode = input("Enter Mode: ")

    if mode == 'v':
        ViewPasswords()
    elif mode == 'a':
        AddPassword()
    elif mode == 'm':
        ManagePasswords()
    elif mode == 'q':
        print("Thank you for using Password Manager.")
        quit()
    else:
        print(mode + " is not a valid mode.")
    End()


def End():
    restart = None
    while restart != 'home' or 'q':
        restart = input("Thank you for using Password Manager. Type 'q' to quit, or 'home' to go to the homepage: ")
        if restart == 'home':
            Introduction()
        elif restart == 'q':
            print("Thank you for using Password Manager.")
            quit()
        else:
            print("Command not recognized. Please enter 'home' for homepage, or 'q' to quit.")


Introduction() #starts program