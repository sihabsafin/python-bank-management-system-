from abc import ABC


class User(ABC):
    def __init__(self, name, email, address, password):
        self.name = name
        self.email = email
        self.address = address
        self.password = password


class Account(User):
    def __init__(self, name, email, address, password, account_type):
        super().__init__(name, email, address, password)
        self.account_type = account_type
        self.__balance = 0
        self.account_number = f"{name.lower()}-{email}"
        self.transaction_history = []
        self.loan_count = 2

    def deposit_balance(self, bank, amount):
        self.__balance += amount
        bank.total_balance += amount
        self.transaction_history.append({"Deposit": amount})
        print(f"\n{amount} TK Deposit Successfully!")

    def withdrawal_balance(self, bank, amount):
        if bank.isBankrupt == False:
            if amount <= self.__balance:
                self.__balance -= amount
                bank.total_balance -= amount
                print(f"\n{amount} TK Withdrawal Successfully!")
                self.transaction_history.append({"Withdrawal": amount})
            else:
                print("Withdrawal amount exceeded")
        else:
            print("The bank is bankrupt!")

    @property
    def check_balance(self):
        return self.__balance

    @check_balance.setter
    def check_balance(self, amount):
        self.__balance = amount

    def check_transaction_history(self):
        print("*************** Transactions History ****************")
        for transaction in self.transaction_history:
            for key, value in transaction.items():
                print(f"Transaction Type: {key}, Amount: {value}")

    def take_loan(self, bank, amount):
        if bank.isLoan:
            if self.loan_count != 0:
                self.__balance += amount
                self.loan_count -= 1
                bank.total_loan += amount
                self.transaction_history.append({"Loan": amount})
                print("\nLoan request successful!")
            else:
                print("\nLoan limit exceeded!")
        else:
            print("\nLoan feature is currently unavailable!")

    def transfer_balance(self, bank, account_number, amount):
        if account_number in bank.accounts:
            if amount <= self.__balance:
                bank.accounts[account_number].check_balance += amount
                self.__balance -= amount
                self.transaction_history.append({"Transfer Money": amount})
                bank.accounts[account_number].transaction_history.append(
                    {"Received Money": amount}
                )
                print("\nMoney Transfer successful !")
            else:
                print("\nTransfer amount exceeded!")
        else:
            print("\nAccount does not exist!")


class Bank:
    def __init__(self, name):
        self.name = name
        self.__total_balance = 0
        self.accounts = {}
        self.isBankrupt = False
        self.isLoan = True
        self.total_loan = 0
        self.admins = {}

    def create_account(self, account):
        self.accounts[account.account_number] = account
        return account

    def delete_account(self, account_number):
        if account_number in self.accounts:
            self.accounts.pop(account_number)
            print(f"This {account_number} account deleted successfully!")
        else:
            print("Account does not exist!")

    def show_users(self):
        print("\n************ Accounts List ************")
        for key, value in self.accounts.items():
            print(
                f"Account NO: {key}, Name: {value.name}, Email: {value.email}, Account Type: {value.account_type}"
            )

    @property
    def total_balance(self):
        return self.__total_balance

    @total_balance.setter
    def total_balance(self, amount):
        self.__total_balance = amount

    def check_total_loan(self):
        return self.total_loan

    def off_loan(self):
        self.isLoan = False
        print("\nLoan feature turned off!")

    def on_loan(self):
        self.isLoan = True
        print("\nLoan feature turned on!")

    def off_bankrupt(self):
        self.isBankrupt = False
        print("\nBankrupt is off!")

    def on_bankrupt(self):
        self.isBankrupt = True
        print("\nBankrupt is on!")


# replica system
abc_bank = Bank("ABC Bank")

admin = Account("Mahfuz", "admin@mail.com", "Dhaka", 123, "Admin")
abc_bank.create_account(admin)
user1 = Account("Nokib", "nokib@mail.com", "Dhaka", 123, "Current")
user2 = Account("Rizan", "rizan@mail.com", "Dhaka", 123, "Current")
abc_bank.create_account(user1)
abc_bank.create_account(user2)

current_user = None
while True:
    if current_user == None:
        ch = input("\nLogin ? Register ? Exit (L/R/X): ")
        if ch == "R":
            print("\n1. Create User Account")
            print("2. Create Admin Account")
            print("3. Main Menu")

            ch = int(input("Enter Your Choice: "))
            if ch == 1:
                name = input("\tEnter your name: ")
                email = input("\tEnter your email: ")
                address = input("\tEnter your address: ")
                password = int(input("\tEnter your password: "))
                account_type = input("\tEnter your account type: ")
                user = Account(name, email, address, password, account_type)
                current_user = abc_bank.create_account(user)
            elif ch == 2:
                name = input("\tEnter your name: ")
                email = input("\tEnter your email: ")
                address = input("\tEnter your address: ")
                password = int(input("\tEnter your password: "))
                account_type = "Admin"
                user = Account(name, email, address, password, account_type)
                current_user = abc_bank.create_account(user)
            elif ch == 3:
                current_user = None
            else:
                print("\nInvalid Input!")
        elif ch == "L":
            print("1. Admin Login")
            print("2. User Login")
            print("3. Main Menu")

            ch = int(input("Enter Your Choice:"))
            if ch == 1 or ch == 2:
                email = input("\tEnter Email: ")
                password = int(input("\tEnter your password: "))
                valid_account = False
                for _, account in abc_bank.accounts.items():
                    if account.email == email and account.password == password:
                        valid_account = True
                        current_user = account
                        break
                if valid_account == False:
                    print("\n\tInvalid Email Or Password!")

            elif ch == 3:
                current_user = None
            else:
                print("\nInvalid Input!")

        elif ch == "X":
            break
        else:
            print("\nInvalid Input!")

    if current_user:
        if current_user.account_type.lower() == "admin":
            print(f"\n**************** Admin Panel ****************")
            print(f"Welcome {current_user.name}...!")
            print("\n\t1.  Show All User")
            print("\t2.  Delete User")
            print("\t3.  Check Balance")
            print("\t4.  Check Total Loan")
            print("\t5.  Turn Off Loan")
            print("\t6.  Turn On Loan")
            print("\t7.  Turn On Bankrupt")
            print("\t8.  Turn Off Bankrupt")
            print("\t9. Log Out")

            ch = int(input("Enter Your Choice: "))
            if ch == 1:
                abc_bank.show_users()
            elif ch == 2:
                account_number = input("Enter User Account Number: ")
                abc_bank.delete_account(account_number)
            elif ch == 3:
                print(f"\n\tTotal Balance: {abc_bank.total_balance}")
            elif ch == 4:
                print(f"\n\tTotal Loan: {abc_bank.check_total_loan()}")
            elif ch == 5:
                abc_bank.off_loan()
            elif ch == 6:
                abc_bank.on_loan()
            elif ch == 7:
                abc_bank.on_bankrupt()
            elif ch == 8:
                abc_bank.off_bankrupt()
            elif ch == 9:
                current_user = None
            else:
                print("\nInvalid Input!")
        else:
            print("\n********** User Panel **********")
            print(f"Welcome {current_user.name}...")
            print("\n\t1. Check Balance")
            print("\t2. Deposit Balance")
            print("\t3. Withdrawal Balance")
            print("\t4. Check Transaction History")
            print("\t5. Transfer Money")
            print("\t6. Take Loan")
            print("\t7. Log Out")

            ch = int(input("Enter Your Choice: "))
            if ch == 1:
                print(f"\n\tBalance: {current_user.check_balance}")
            elif ch == 2:
                amount = int(input("Enter Amount: "))
                current_user.deposit_balance(abc_bank, amount)
            elif ch == 3:
                amount = int(input("Enter Amount: "))
                current_user.withdrawal_balance(abc_bank, amount)
            elif ch == 4:
                current_user.check_transaction_history()
            elif ch == 5:
                account_number = input("Enter User Account Number: ")
                amount = int(input("Enter Amount: "))
                current_user.transfer_balance(abc_bank, account_number, amount)
            elif ch == 6:
                amount = int(input("Enter Amount: "))
                current_user.take_loan(abc_bank, amount)
            elif ch == 7:
                current_user = None
            else:
                print("\nInvalid Input!")
