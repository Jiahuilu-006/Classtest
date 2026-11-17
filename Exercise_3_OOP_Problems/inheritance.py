"""Inheritance exercises, Problems 1–3 from the teacher's OOP handout."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation


# Problem 1
class Vehicle:
    def drive(self) -> str:
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self) -> str:
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self) -> str:
        return "Riding a bicycle"


# Problem 2
class Person:
    def __init__(self, name: str, age: int, address: str):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self) -> str:
        return f"Hi, I'm {self.name}, {self.age} years old, from {self.address}."


class Student(Person):
    def __init__(self, name: str, age: int, address: str, field_of_study: str):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self) -> str:
        return f"{super().introduce()} I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name: str, age: int, address: str, company: str):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self) -> str:
        return f"{super().introduce()} I work at {self.company}."


# Problem 3
def _money(value: int | float | str | Decimal) -> Decimal:
    """Convert monetary input to Decimal and reject invalid/non-finite values."""
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Amount must be a valid number") from exc
    if not number.is_finite():
        raise ValueError("Amount must be finite")
    return number


class BankAccount:
    def __init__(self, account_number: str, balance: int | float | str | Decimal = 0):
        self.account_number = account_number
        self.balance = _money(balance)
        if self.balance < 0:
            raise ValueError("Initial balance cannot be negative")

    def deposit(self, amount: int | float | str | Decimal) -> None:
        amount = _money(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: int | float | str | Decimal) -> bool:
        amount = _money(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(
        self,
        destination: "BankAccount",
        amount: int | float | str | Decimal,
    ) -> bool:
        if not isinstance(destination, BankAccount):
            raise TypeError("Destination must be a BankAccount")
        amount = _money(amount)
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > self.balance:
            return False
        if destination is self:
            return True  # A transfer to the same account changes nothing.
        self.balance -= amount
        destination.balance += amount
        return True


class SavingsAccount(BankAccount):
    def __init__(
        self,
        account_number: str,
        balance: int | float | str | Decimal = 0,
        interest_rate: int | float | str | Decimal = 0,
    ):
        super().__init__(account_number, balance)
        self.interest_rate = _money(interest_rate)
        if self.interest_rate < 0:
            raise ValueError("Interest rate cannot be negative")

    def add_interest(self) -> Decimal:
        """Apply interest_rate as a fraction (0.05 means 5%)."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def check_balance(self) -> Decimal:
        return self.balance


if __name__ == "__main__":
    for vehicle in (Vehicle(), Car(), Bicycle()):
        print(vehicle.drive())

    for person in (
        Person("Alex", 23, "Paris"),
        Student("Sam", 20, "Lyon", "Computer Science"),
        Employee("Pat", 28, "Nice", "Example Company"),
    ):
        print(person.introduce())

    current = BankAccount("A001", "100")
    savings = SavingsAccount("S001", "50", "0.05")
    print("Transfer succeeds:", current.transfer(savings, "25"))
    print("Interest added:", savings.add_interest())
    print("Savings balance:", savings.check_balance())
