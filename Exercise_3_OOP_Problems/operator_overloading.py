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
