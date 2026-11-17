# Exercise 3 — COMPLETE OOP Problems (All answers in ONE file)

This document contains **all 9 problems** from the original OOP exercise, including the complete Python solutions for **Operator Overloading (6 problems)** and **Inheritance (3 problems)**. It is intended to be the **single submission link**.

The original exercise skips Operator Overloading Problem 3; therefore, the original problem numbers are preserved.

## Part 1 — Operator Overloading

| Problem | Requirement |
| --- | --- |
| 1 | Complex number addition and subtraction |
| 2 | Compare two persons by age using `>` |
| 4 | 3D vector dot product using `*` |
| 5 | All six Circle comparisons based on radius |
| 6 | 2D point comparisons based on distance from origin |
| 7 | Matrix multiplication using `*` |

The following is the **full solution** to Part 1.

```python
"""Operator overloading exercises, using the numbering in the teacher's handout.

Problem 3 is not present in the supplied exercise statement.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ComplexNumber:
    """Problem 1: addition and subtraction of two complex numbers."""
    real: float
    imaginary: float

    def __add__(self, other: object):
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)

    def __sub__(self, other: object):
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)

    def __str__(self) -> str:
        sign = "+" if self.imaginary >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imaginary)}i"


@dataclass
class Person:
    """Problem 2: compare people by age using >."""
    name: str
    age: int
    gender: str

    def __gt__(self, other: object):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age


@dataclass(frozen=True)
class Vector:
    """Problem 4: multiply two 3D vectors to get their dot product."""
    x: float
    y: float
    z: float

    def __mul__(self, other: object):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z


@dataclass(frozen=True, eq=False)
class Circle:
    """Problem 5: compare circles using their radii."""
    radius: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.radius) or self.radius < 0:
            raise ValueError("Radius must be a finite, non-negative number")

    def __lt__(self, other: object):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __gt__(self, other: object):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius

    def __eq__(self, other: object):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __ne__(self, other: object):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius != other.radius

    def __ge__(self, other: object):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius >= other.radius

    def __le__(self, other: object):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius <= other.radius


@dataclass(frozen=True, eq=False)
class Point2D:
    """Problem 6: compare points by Euclidean distance to (0, 0)."""
    x: float
    y: float

    @property
    def distance(self) -> float:
        return math.hypot(self.x, self.y)

    def __lt__(self, other: object):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance < other.distance

    def __gt__(self, other: object):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance > other.distance

    def __eq__(self, other: object):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance == other.distance

    def __ne__(self, other: object):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance != other.distance

    def __ge__(self, other: object):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance >= other.distance

    def __le__(self, other: object):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance <= other.distance


class Matrix:
    """Problem 7: matrix multiplication using * (not element-wise multiplication)."""

    def __init__(self, rows: Sequence[Sequence[float]]):
        if not rows or not rows[0]:
            raise ValueError("A matrix must have at least one row and column")
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("All matrix rows must have the same length")
        self.rows = tuple(tuple(row) for row in rows)

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0])

    def __mul__(self, other: object):
        if not isinstance(other, Matrix):
            return NotImplemented
        left_rows, left_cols = self.shape
        right_rows, right_cols = other.shape
        if left_cols != right_rows:
            raise ValueError(
                f"Cannot multiply matrices of shapes {self.shape} and {other.shape}"
            )
        result = [
            [
                sum(self.rows[i][k] * other.rows[k][j] for k in range(left_cols))
                for j in range(right_cols)
            ]
            for i in range(left_rows)
        ]
        return Matrix(result)

    def __eq__(self, other: object):
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    def __repr__(self) -> str:
        return f"Matrix({[list(row) for row in self.rows]!r})"


if __name__ == "__main__":
    print("P1:", ComplexNumber(2, 3) + ComplexNumber(4, -1))
    print("P1:", ComplexNumber(2, 3) - ComplexNumber(4, -1))
    print("P2:", Person("Alex", 22, "M") > Person("Sam", 20, "F"))
    print("P4:", Vector(1, 2, 3) * Vector(4, 5, 6))
    print("P5:", Circle(3) < Circle(5))
    print("P6:", Point2D(3, 4) == Point2D(0, 5))
    print("P7:", Matrix([[1, 2], [3, 4]]) * Matrix([[5, 6], [7, 8]]))
```

## Part 2 — Inheritance

| Problem | Requirement |
| --- | --- |
| 1 | Override `Vehicle.drive()` in `Car` and `Bicycle` |
| 2 | Extend `Person` with `Student` and `Employee` and personalized introductions |
| 3 | `BankAccount` and `SavingsAccount`, including deposits, withdrawals, transfers, interest and balance checks |

The following is the **full solution** to Part 2.

```python
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
```

## How to run the solutions

Both complete source files are also kept in the repository as independently runnable modules, because **each part defines a different `Person` class**. Keeping them in separate modules prevents a naming conflict when running them.

```bash
python Exercise_3_OOP_Problems/operator_overloading.py
python Exercise_3_OOP_Problems/inheritance.py
python -m unittest discover -s Exercise_3_OOP_Problems -v
```

The test source is available in [test_oop_problems.py](test_oop_problems.py).

**For submission, use the URL of this page. You do not need to submit separate Part 1 and Part 2 links.**
