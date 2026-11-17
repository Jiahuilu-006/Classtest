"""Unit tests for the hospital UML implementation (Python standard library)."""
import unittest
from decimal import Decimal

from hospital import (
    CashPayment, CheckPayment, CreditCardPayment, Doctor, HealthProblem,
    Organizer, Patient, Payment, PaymentStatus, ProblemStatus,
)


class HospitalTests(unittest.TestCase):
    def setUp(self):
        self.patient = Patient("Alex", "alex@example.com")
        self.doctor = Doctor("Dr Smith", "smith@example.com", specialty="General")
        self.organizer = Organizer("Sam", "sam@example.com")
        self.problem = self.patient.submit_problem("Headache")

    def test_patient_submits_problem(self):
        self.assertEqual(self.problem.status, ProblemStatus.PENDING)
        self.assertIs(self.problem.patient, self.patient)
        self.assertIn(self.problem, self.patient.problems)

    def test_empty_problem_rejected(self):
        with self.assertRaises(ValueError):
            self.patient.submit_problem("  ")

    def test_doctor_assignment_and_prescription(self):
        self.organizer.assign_doctor(self.problem, self.doctor)
        self.doctor.review(self.problem)
        prescription = self.doctor.prescribe(self.problem, "Drink water")
        self.organizer.deliver_prescription(prescription)
        self.problem.resolve()
        self.assertTrue(prescription.delivered)
        self.assertEqual(self.problem.status, ProblemStatus.RESOLVED)

    def test_unassigned_doctor_cannot_prescribe(self):
        with self.assertRaises(ValueError):
            self.doctor.prescribe(self.problem, "Rest")

    def test_cannot_resolve_before_delivery(self):
        with self.assertRaises(ValueError):
            self.problem.resolve()

    def test_successful_cash_payment_and_forwarding(self):
        self.organizer.assign_doctor(self.problem, self.doctor)
        payment = Payment(self.problem, Decimal("20"), CashPayment(Decimal("25")), "key-1")
        self.assertTrue(payment.process())
        self.organizer.forward_payment(payment)
        self.assertEqual(payment.status, PaymentStatus.FORWARDED)

    def test_declined_card_payment(self):
        payment = Payment(self.problem, Decimal("20"), CreditCardPayment(False), "key-2")
        self.assertFalse(payment.process())
        self.assertEqual(payment.status, PaymentStatus.FAILED)

    def test_check_payment(self):
        payment = Payment(self.problem, Decimal("20"), CheckPayment("CHECK-123"), "key-3")
        self.assertTrue(payment.process())

    def test_cannot_charge_twice(self):
        payment = Payment(self.problem, Decimal("20"), CreditCardPayment(), "key-4")
        payment.process()
        with self.assertRaises(ValueError):
            payment.process()

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            Payment(self.problem, Decimal("-1"), CashPayment(Decimal("5")), "key-5")

    def test_other_organizer_cannot_forward(self):
        payment = Payment(self.problem, Decimal("20"), CreditCardPayment(), "key-6")
        payment.process()
        with self.assertRaises(ValueError):
            self.organizer.forward_payment(payment)


if __name__ == "__main__":
    unittest.main()
