class BankAccount:
    def __init__(self, id, name, balance):

        self.__id = id
        self.__name = name
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount
    def withdraw(self, amont):
        self.__balance -= amont
    def __str__(self):
        return "{0}, {1}, {2}".format(self.__id, self.__name, self.__balance)
    
accont1 = BankAccount(100, "전우치", 15000)
accont1.withdraw(3000)

print(accont1)