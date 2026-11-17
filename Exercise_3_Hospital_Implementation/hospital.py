"""Small implementation of the hospital UML practice model.

This is a learning exercise, not a production medical/payment service.
Payments are simulated; no real card data or transactions are processed.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Protocol
from uuid import uuid4


class ProblemStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"


class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    FORWARDED = "forwarded"


@dataclass
class User:
    name: str
    email: str
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Patient(User):
    problems: list["HealthProblem"] = field(default_factory=list)

    def submit_problem(self, description: str) -> "HealthProblem":
        if not description.strip():
            raise ValueError("The problem description cannot be empty")
        problem = HealthProblem(patient=self, description=description)
        self.problems.append(problem)
        return problem


@dataclass
class Doctor(User):
    specialty: str = ""

    def review(self, problem: "HealthProblem") -> None:
        if problem.doctor is not self:
            raise ValueError("Doctor is not assigned to this case")
        problem.status = ProblemStatus.IN_REVIEW

    def prescribe(self, problem: "HealthProblem", details: str) -> "Prescription":
        if problem.doctor is not self or problem.status != ProblemStatus.IN_REVIEW:
            raise ValueError("Review the assigned case before prescribing")
        if not details.strip():
            raise ValueError("Prescription details cannot be empty")
        prescription = Prescription(problem=problem, doctor=self, details=details)
        problem.prescriptions.append(prescription)
        return prescription


@dataclass
class Organizer(User):
    def assign_doctor(self, problem: "HealthProblem", doctor: Doctor) -> None:
        if problem.status == ProblemStatus.RESOLVED:
            raise ValueError("A resolved case cannot be reassigned")
        problem.doctor = doctor
        problem.organizer = self

    def deliver_prescription(self, prescription: "Prescription") -> None:
        if prescription.problem.organizer is not self:
            raise ValueError("Organizer does not manage this case")
        prescription.delivered = True

    def forward_payment(self, payment: "Payment") -> None:
        if payment.problem.organizer is not self:
            raise ValueError("Organizer does not manage this case")
        if payment.status != PaymentStatus.SUCCEEDED:
            raise ValueError("Only successful payments can be forwarded")
        payment.status = PaymentStatus.FORWARDED


@dataclass
class HealthProblem:
    patient: Patient
    description: str
    id: str = field(default_factory=lambda: str(uuid4()))
    status: ProblemStatus = ProblemStatus.PENDING
    doctor: Doctor | None = None
    organizer: Organizer | None = None
    prescriptions: list["Prescription"] = field(default_factory=list)

    def resolve(self) -> None:
        if not self.prescriptions or not any(p.delivered for p in self.prescriptions):
            raise ValueError("Deliver a prescription before resolving the case")
        self.status = ProblemStatus.RESOLVED


@dataclass
class Prescription:
    problem: HealthProblem
    doctor: Doctor
    details: str
    id: str = field(default_factory=lambda: str(uuid4()))
    delivered: bool = False


class PaymentMethod(Protocol):
    def process(self, amount: Decimal) -> bool:
        """Return whether a *simulated* payment succeeds."""
        ...


@dataclass
class CashPayment:
    amount_received: Decimal

    def process(self, amount: Decimal) -> bool:
        return self.amount_received >= amount


@dataclass
class CheckPayment:
    check_number: str

    def process(self, amount: Decimal) -> bool:
        return bool(self.check_number.strip()) and amount > 0


@dataclass
class CreditCardPayment:
    approved: bool = True  # Simulated authorization, not a real card number.

    def process(self, amount: Decimal) -> bool:
        return self.approved and amount > 0


@dataclass
class Payment:
    problem: HealthProblem
    amount: Decimal
    method: PaymentMethod
    idempotency_key: str
    status: PaymentStatus = PaymentStatus.PENDING

    def __post_init__(self) -> None:
        if not self.amount.is_finite() or self.amount <= 0:
            raise ValueError("Payment amount must be positive and finite")
        if not self.idempotency_key.strip():
            raise ValueError("An idempotency key is required")

    def process(self) -> bool:
        # One attempt per Payment object: repeat calls cannot charge twice.
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Payment was already processed")
        successful = self.method.process(self.amount)
        self.status = PaymentStatus.SUCCEEDED if successful else PaymentStatus.FAILED
        return successful


if __name__ == "__main__":
    patient = Patient(name="Alex", email="alex@example.com")
    doctor = Doctor(name="Dr Smith", email="smith@example.com", specialty="General")
    organizer = Organizer(name="Sam", email="sam@example.com")
    case = patient.submit_problem("Persistent headache")
    organizer.assign_doctor(case, doctor)
    doctor.review(case)
    prescription = doctor.prescribe(case, "Rest and follow up if symptoms persist")
    organizer.deliver_prescription(prescription)
    case.resolve()
    payment = Payment(case, Decimal("25.00"), CashPayment(Decimal("30")), "demo-1")
    print("Payment accepted:", payment.process())
    organizer.forward_payment(payment)
    print("Case status:", case.status.value)
