# Exercise 3 — OOP Problems (teacher's original questions)

This folder solves the OOP Problems provided in the course.

## A. Operator Overloading

| Original problem number | Topic | Class |
| --- | --- | --- |
| Problem 1 | Add/subtract complex numbers (+ and -) | ComplexNumber |
| Problem 2 | Compare people's ages with > | Person |
| Problem 4 | 3D vector dot product with * | Vector |
| Problem 5 | All six radius-based circle comparisons | Circle |
| Problem 6 | Compare 2D points by distance from origin | Point2D |
| Problem 7 | Matrix multiplication with * | Matrix |

**Problem 3 was not included in the supplied question sheet.** The original numbering is retained.

Solution: [operator_overloading.py](operator_overloading.py)

## B. Inheritance

| Problem | Topic | Classes |
| --- | --- | --- |
| Problem 1 | Override drive() | Vehicle, Car, Bicycle |
| Problem 2 | Inherit and personalize introduce() | Person, Student, Employee |
| Problem 3 | Deposit, withdrawal, savings interest and transfers | BankAccount, SavingsAccount |

Solution: [inheritance.py](inheritance.py)

## Run

Use Python 3.10+; no external dependencies are required.

From inside this folder:

\`\`\`bash
python operator_overloading.py
python inheritance.py
python -m unittest discover -v
\`\`\`

Or, from the repository root:

\`\`\`bash
python -m unittest discover -s Exercise_3_OOP_Problems -v
\`\`\`

The two sections each define a Person class for different exercises, so they are kept in separate Python modules. Bank account amounts use Decimal to avoid ordinary binary floating-point rounding issues. Interest rate is a fraction (e.g. 0.05 means 5%).

**Submission:** You can submit this README link for the entire OOP exercise, or the two individual Python file links if your submission spreadsheet has separate rows.
