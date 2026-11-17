"""Tests for the operator-overloading and inheritance problems."""
import unittest
from decimal import Decimal

from operator_overloading import (
    Circle, ComplexNumber, Matrix, Person as ComparePerson, Point2D, Vector,
)
from inheritance import (
    BankAccount, Bicycle, Car, Employee, Person, SavingsAccount, Student, Vehicle,
)


class OperatorOverloadingTests(unittest.TestCase):
    def test_problem_1_complex_add_subtract(self):
        a, b = ComplexNumber(2, 3), ComplexNumber(4, -1)
        self.assertEqual(a + b, ComplexNumber(6, 2))
        self.assertEqual(a - b, ComplexNumber(-2, 4))

    def test_problem_2_person_age(self):
        self.assertTrue(ComparePerson("A", 25, "F") > ComparePerson("B", 20, "M"))
        self.assertFalse(ComparePerson("A", 20, "F") > ComparePerson("B", 20, "M"))

    def test_problem_4_vector_dot_product(self):
        self.assertEqual(Vector(1, 2, 3) * Vector(4, 5, 6), 32)

    def test_problem_5_all_circle_comparisons(self):
        small, equal, large = Circle(2), Circle(2), Circle(3)
        self.assertTrue(small < large)
        self.assertTrue(large > small)
        self.assertTrue(small == equal)
        self.assertFalse(small != equal)
        self.assertTrue(small != large)
        self.assertTrue(large >= small)
        self.assertTrue(small <= equal)
        self.assertFalse(small >= large)

    def test_problem_6_points_compare_by_origin_distance(self):
        a, b, c = Point2D(3, 4), Point2D(0, 5), Point2D(0, 6)
        self.assertTrue(a == b)
        self.assertFalse(a != b)
        self.assertTrue(a < c)
        self.assertTrue(c > a)
        self.assertTrue(a <= b)
        self.assertTrue(c >= b)

    def test_problem_7_matrix_product(self):
        left = Matrix([[1, 2, 3], [4, 5, 6]])
        right = Matrix([[7, 8], [9, 10], [11, 12]])
        self.assertEqual(left * right, Matrix([[58, 64], [139, 154]]))

    def test_problem_7_invalid_matrix_dimensions(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2], [3]])
        with self.assertRaises(ValueError):
            Matrix([[1, 2]]) * Matrix([[1, 2]])


class InheritanceTests(unittest.TestCase):
    def test_problem_1_vehicle_override(self):
        self.assertEqual(Vehicle().drive(), "Driving a vehicle")
        self.assertEqual(Car().drive(), "Driving a car")
        self.assertEqual(Bicycle().drive(), "Riding a bicycle")

    def test_problem_2_person_and_subclasses(self):
        base = Person("Alex", 22, "Paris")
        student = Student("Sam", 19, "Paris", "Physics")
        employee = Employee("Pat", 30, "Lyon", "ABC Corp")
        self.assertIn("Alex", base.introduce())
        self.assertIn("Physics", student.introduce())
        self.assertIn("ABC Corp", employee.introduce())
        self.assertIsInstance(student, Person)
        self.assertIsInstance(employee, Person)

    def test_problem_3_bank_deposit_withdraw(self):
        account = BankAccount("001", "100")
        account.deposit("25.50")
        self.assertEqual(account.balance, Decimal("125.50"))
        self.assertTrue(account.withdraw("5.50"))
        self.assertFalse(account.withdraw("500"))
        self.assertEqual(account.balance, Decimal("120.00"))

    def test_problem_3_transfer(self):
        source = BankAccount("001", "100")
        destination = SavingsAccount("002", "40", "0.05")
        self.assertTrue(source.transfer(destination, "30"))
        self.assertEqual(source.balance, Decimal("70"))
        self.assertEqual(destination.check_balance(), Decimal("70"))
        self.assertFalse(source.transfer(destination, "100"))
        self.assertEqual(source.balance, Decimal("70"))
        self.assertEqual(destination.check_balance(), Decimal("70"))

    def test_problem_3_interest(self):
        savings = SavingsAccount("002", "200", "0.05")
        self.assertEqual(savings.add_interest(), Decimal("10.00"))
        self.assertEqual(savings.check_balance(), Decimal("210.00"))

    def test_invalid_bank_amount(self):
        account = BankAccount("001", "10")
        with self.assertRaises(ValueError):
            account.deposit("-3")
        with self.assertRaises(ValueError):
            account.withdraw("0")
        with self.assertRaises(ValueError):
            account.transfer(BankAccount("002"), "-1")


if __name__ == "__main__":
    unittest.main()
