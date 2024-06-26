#jigme namgyel
# first year electrical 
#02230064
# module code: CSF101

#Reference
#https://www.blackbox.ai
#https://chatgpt.com/?oai-dm=1
#Copilot
#Youtube

import random # import random module
import os  ##This is particularly useful for tasks like file manipulation,that's why it’s used in the banking application script to read from and write to a text file.

# Define Account class
class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        # Constructor to initialize account attributes
        self.account_number = account_number # get default account number
        self.password = password # initalize password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        # Method to deposit money into the account
        self.balance += amount
        print(f"Deposited Nu.{amount}. And your New balance is Nu.{self.balance}")

    def withdraw(self, amount):
        # Method to withdraw money from the account
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdraw Nu.{amount} and your New balance is Nu.{self.balance}")  # Withdrawal successful

        else:
            print("Insufficient funds")
            return False  # Withdrawal unsuccessful due to insufficient funds

    def __str__(self):
        # String representation of the account
        return f"Account Number: {self.account_number}\nAccount Type: {self.account_type}\nBalance: {self.balance}"


# Define Bank class
class Bank:
    def __init__(self):
        # initialize the bank with an empty dictionary of accounts
        self.accounts = {}

    def create_account(self, account_type,):
        # Method to create a new account
        account_number = random.randint(100000000, 999999999)  # Generate a random account number
        password = input("Create a password: ")  # asking userinput to create a password
        account = Account(account_number, password, account_type)
        self.accounts[account_number] = account  # Add the account to the dictionary
        self.save_account_info(account)  # Save account information to file
        return account

    def save_account_info(self, account):
        # Method to save account information to a file
        with open("accounts.txt", "a") as file:
            file.write(
                f"{account.account_number},{account.password},{account.account_type} Nu.{account.balance} \n"
            )

    def load_accounts(self):
    # Method to load accounts from file into memory
        if os.path.exists("accounts.txt"):  # Check if file exists
            with open("accounts.txt", "r") as file:#If the file exists, it opens the file in read mode ('r')
                lines = file.readlines()  # Read all lines from the file
                for line in lines:#The method iterates over each line in the lines list.
                    account_data = line.strip().split(",")  # Split each line into account data using comma as delimiter
                    account_number, password, account_type, balance = account_data  # Unpack the account data
                # Create a new Account object with the unpacked data and add it to the accounts dictionary
                    self.accounts[int(account_number)] = Account(
                    int(account_number), password, account_type, float(balance)
                    )


    def authenticate(self, account_number, password):
        # Method to authenticate a user based on account number and password
        account = self.accounts.get(account_number)
        if account and account.password == password: # check whethere the password entered matches the the old password
            return account
        else:
            return None

    def delete_account(self, account_number):
        # Method to delete an account
        if account_number in self.accounts: # chcking whgethe the account exist in self.account or not
            del self.accounts[account_number]
            self.update_file() # return the updated file

    def update_file(self):
        # Method to update the file with account information
        with open("accounts.txt", "w") as file: #Opens the file "accounts.txt" in write mode ('w') for updating account information.
            for account_number, account in self.accounts.items(): #Iterates over each account in the dictionary 'self.accounts', where account numbers are keys and account objects are values.
                file.write(
                    f"{account.account_number},{account.password},{account.account_type},{account.balance}\n" # Writes each account's information (account number, password, account type, and balance) to the file in a comma-separated format.
                )                    # and Each account's information is written on a new line in the file.

    def transfer_money(self, sender_account_number, receiver_account_number, amount):
        # Method to transfer money from one account to another
        sender_account = self.accounts.get(sender_account_number)
        receiver_account = self.accounts.get(receiver_account_number)
        if sender_account and receiver_account:
            if sender_account.balance >= amount:
                sender_account.withdraw(amount)
                receiver_account.deposit(amount)
                self.update_file()
                print("Transfer successful.")
                print(f"Transferred Nu.{amount} to account {receiver_account.account_number}")
            else:
                print("Insufficient funds.")
        else:
            print("One or both accounts do not exist.")
        


# Define main function
def main():
    bank = Bank()
    bank.load_accounts()

    while True:         # Banking application
        print("\nWelcome to the Bank of Bhutan!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice option number:\n ")

        if choice == "1":
            account_type = input("Enter account type (Personal/Business): ").capitalize()# asking for the type of account
            name = input("Enter your full name:\n")
            account = bank.create_account(account_type)
            print(" Your Account is created successfully!Thank you!")          # return Output with name, default account number and with created account password.
            print(f"Mr/Mrs. {name } Your account number is: {account.account_number}")
            print(f"Mr/Mrs. {name } Your password is: {account.password}")

        elif choice == "2":
            account_number = int(input("Enter account number: "))
            password = input("Enter your password: ")
            account = bank.authenticate(account_number, password) # check whethere account number and password are correct or not
            if account:
                print(" Your Login successful!")
                while True:
                    print("\n1. Check Balance") # option after your login
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Delete Account")
                    print("5. Transfer Money")
                    print("6. Logout")
                    option = input("Enter your choice: ")

                    if option == "1":
                        print(f" Nu. {account}")

                    elif option == "2":
                        amount = float(input("Enter amount to deposit: "))
                        new_balance = account.deposit(amount)
                        bank.update_file()
                       

                    elif option == "3": # withdraw option
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            bank.update_file()
                         

                    elif option == "4": # account deletion
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == "yes":
                            bank.delete_account(account_number)
                            print("Account deleted successfully.")
                            break

                    elif option == "5":
                        receiver_account_number = int(input("Enter receiver's account number: "))
                        amount = float(input("Enter amount to transfer: "))
                        bank.transfer_money(account_number, receiver_account_number, amount) # sending money from account_number(sender) to receiver_number

                    elif option == "6":
                        print("Logged out successfully.")
                        break

                    else:
                        print("Invalid option!")

            else:
                print("Invalid account number or password!")

        elif choice == "3": # Exit option
            print("Thank you for visitiong Bank of Bhutan. Goodbye!")
            break # code stop

        else:
            print("Invalid choice!")


if __name__ == "__main__":#in Python checks if the script is being run directly by the interpreter, rather than being imported as a module into another script.
    main()
