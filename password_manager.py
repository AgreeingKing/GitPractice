users = {"Wian": "123", "Tiaan": "123"}


def list_users():
    for user, password in users.items():
        print("-" * 50)
        print(f"User: {user}")
        print(f"Password: {password}")
    print("-" * 50)


def add_user():
    while True:
        username = input("\nPlease enter the new users name:\n")
        if username in users:
            print("\nUser already exists.\n")
        else:
            break

    user_password = input("\nPlease enter the new users password\n")
    if confirm(input("\nConfirm? (Y/N)\n")):
        users[username] = user_password
        print("\nUser added successfully!\n")
    else:
        print("\nOperation cancelled!\n")


def remove_user():
    while True:
        user_to_delete = input("\nEnter the users name that you want to delete:\n")
        if user_to_delete in users:
            if confirm(input(f"\nConfirm deletion of user: {user_to_delete}? (Y/N)\n")):
                del users[user_to_delete]
                print("\nUser successfully deleted.\n")
                break
            else:
                print("\nOperation cancelled!\n")
                break
        else:
            print("\nUser not found!\n")


# Small function to confirm "Yes/No" answers
def confirm(answer=str):
    answer = answer.lower().strip()
    # Preventing endless loop with retry limit.
    retries = 3
    while retries > 0:
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            answer = input("\nPlease enter Y (Yes) or N (No).\n").lower()
        retries -= 1
    print("Too many invalid entries. Defaulting to No.")
    return False


print(
    """
You Shall Not Pass(word)!!!
Welcome to the password manager!
"""
)

while True:
    menu_option = input(
        """Main Menu:

1. Add User
2. Remove User
3. List Users
4. Exit

:"""
    )

    if menu_option == "1":
        add_user()
    elif menu_option == "2":
        remove_user()
    elif menu_option == "3":
        list_users()
    elif menu_option == "4":
        exit()
    else:
        print("\nPlease choose a valid option!")
