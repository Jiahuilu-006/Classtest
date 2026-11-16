# UML Exercise 1 — Hospital Management System

Solution for Tasks 1–3 from the course UML practice: initial class diagram, expanded model and consultation sequence, advanced model and system sequence diagrams.

## Task 1 — Initial class diagram

The first model has the three requested roles. The associations are refined into case-specific relationships in Task 2.

```plantuml
@startuml
skinparam classAttributeIconSize 0
class Patient {
  - patientId: String
  - name: String
  - email: String
  - passwordHash: String
  + submitProblem(description: String): HealthProblem
  + pay(payment: Payment): PaymentResult
}
class Doctor {
  - doctorId: String
  - name: String
  - specialty: String
  - email: String
  + reviewProblem(problem: HealthProblem): void
  + issuePrescription(problem: HealthProblem, details: String): Prescription
}
class Organizer {
  - organizerId: String
  - name: String
  - email: String
  - passwordHash: String
  + registerPatient(details: PatientDetails): Patient
  + assignDoctor(problem: HealthProblem, doctor: Doctor): void
  + deliverPrescription(prescription: Prescription): void
}
Patient "0..*" -- "0..*" Doctor : consults
Organizer "0..*" -- "0..*" Patient : coordinates care for
Organizer "0..*" -- "0..*" Doctor : coordinates work with
@enduml
```

## Task 2 — Complete class diagram and consultation sequence

The six required core classes are Patient, Doctor, Organizer, HealthProblem, Prescription, and Payment. PaymentMethod plus its concrete implementations model Check, Cash, and CreditCard. Each case has one active doctor and one coordinating organizer; it can have several prescriptions and payment attempts over its history.

```plantuml
@startuml
skinparam classAttributeIconSize 0
class Patient {
  - patientId: String
  - name: String
  - email: String
  - passwordHash: String
  + submitProblem(description: String): HealthProblem
  + pay(payment: Payment): PaymentResult
}
class Doctor {
  - doctorId: String
  - name: String
  - specialty: String
  - email: String
  + reviewProblem(problem: HealthProblem): void
  + issuePrescription(problem: HealthProblem, details: String): Prescription
}
class Organizer {
  - organizerId: String
  - name: String
  - email: String
  - passwordHash: String
  + registerPatient(details: PatientDetails): Patient
  + assignDoctor(problem: HealthProblem, doctor: Doctor): void
  + deliverPrescription(prescription: Prescription): void
  + forwardPayment(payment: Payment, doctor: Doctor): void
}
class HealthProblem {
  - problemId: String
  - description: String
  - status: ProblemStatus
  - createdAt: DateTime
  + updateStatus(status: ProblemStatus): void
  + addPrescription(prescription: Prescription): void
}
class Prescription {
  - prescriptionId: String
  - details: String
  - issuedAt: DateTime
  - deliveredAt: DateTime
  + markDelivered(): void
  + isValid(): Boolean
}
class Payment {
  - paymentId: String
  - amount: Decimal
  - status: PaymentStatus
  - createdAt: DateTime
  + process(): PaymentResult
  + markForwarded(): void
}
interface PaymentMethod {
  + process(amount: Decimal): PaymentResult
}
class CashPayment {
  + process(amount: Decimal): PaymentResult
}
class CheckPayment {
  - checkNumber: String
  + process(amount: Decimal): PaymentResult
}
class CreditCardPayment {
  - authorizationReference: String
  + process(amount: Decimal): PaymentResult
}
Patient "1" *-- "0..*" HealthProblem : submits
Organizer "1" -- "0..*" HealthProblem : coordinates
Doctor "1" -- "0..*" HealthProblem : reviews
HealthProblem "1" *-- "0..*" Prescription : history
Doctor "1" -- "0..*" Prescription : issues
Organizer "0..1" -- "0..*" Prescription : delivers
Patient "1" -- "0..*" Payment : makes
HealthProblem "1" -- "0..*" Payment : is billed for
Organizer "0..1" -- "0..*" Payment : forwards
Payment "1" --> "1" PaymentMethod : uses
PaymentMethod <|.. CashPayment
PaymentMethod <|.. CheckPayment
PaymentMethod <|.. CreditCardPayment
@enduml
```

### Sequence — patient submits a problem, receives a prescription, and pays

```plantuml
@startuml
actor Patient
participant "Hospital System" as System
participant Organizer
participant Doctor
participant HealthProblem
participant Prescription
participant Payment
participant PaymentMethod
Patient -> System: submitProblem(description)
create HealthProblem
System -> HealthProblem: create(description, PENDING)
System -> Organizer: notifyNewProblem(problem)
Organizer -> HealthProblem: assignDoctor(doctor)
Organizer -> Doctor: requestReview(problem)
Doctor -> HealthProblem: review()
Doctor -> HealthProblem: updateStatus(IN_REVIEW)
create Prescription
Doctor -> Prescription: create(details, issuedAt)
Doctor -> HealthProblem: addPrescription(prescription)
Organizer -> System: deliver(prescription, patient)
System -> Prescription: markDelivered()
System -> Patient: notifyPrescription(prescription)
Patient -> System: pay(amount, method)
System -> Payment: create(amount, PENDING)
Payment -> PaymentMethod: process(amount)
PaymentMethod --> Payment: success / failure
alt payment succeeds
  Payment --> System: SUCCEEDED
  System -> Organizer: forwardPayment(payment, doctor)
  Organizer -> Doctor: transfer(amount)
  Payment -> Payment: markForwarded()
  System --> Patient: receipt
else payment fails
  Payment --> System: FAILED
  System --> Patient: paymentFailure
end
System -> HealthProblem: updateStatus(RESOLVED)
@enduml
```

## Task 3 — Advanced class model

This version adds the shared User superclass, status tracking, timestamps, prescription history and polymorphic payment strategies. Passwords are stored as hashes; card details are handled by a payment provider rather than retained by the hospital system.

```plantuml
@startuml
skinparam classAttributeIconSize 0
abstract class User {
  - id: String
  - name: String
  - email: String
  - passwordHash: String
  + login(email: String, password: String): Boolean
  + logout(): void
}
class Patient {
  - phone: String
  - address: String
  + submitProblem(description: String): HealthProblem
  + pay(payment: Payment): PaymentResult
}
class Doctor {
  - specialty: String
  - licenseNumber: String
  + reviewProblem(problem: HealthProblem): void
  + issuePrescription(problem: HealthProblem, details: String): Prescription
}
class Organizer {
  - department: String
  + registerPatient(details: PatientDetails): Patient
  + assignDoctor(problem: HealthProblem, doctor: Doctor): void
  + deliverPrescription(prescription: Prescription): void
  + forwardPayment(payment: Payment, doctor: Doctor): void
}
User <|-- Patient
User <|-- Doctor
User <|-- Organizer

class HealthProblem {
  - problemId: String
  - description: String
  - status: ProblemStatus
  - createdAt: DateTime
  - updatedAt: DateTime
  - resolvedAt: DateTime
  + updateStatus(status: ProblemStatus): void
  + addPrescription(prescription: Prescription): void
}
enum ProblemStatus {
  PENDING
  IN_REVIEW
  RESOLVED
}
class Prescription {
  - prescriptionId: String
  - details: String
  - issuedAt: DateTime
  - deliveredAt: DateTime
  - validUntil: DateTime
  + markDelivered(): void
  + isValid(): Boolean
}
class Payment {
  - paymentId: String
  - amount: Decimal
  - status: PaymentStatus
  - createdAt: DateTime
  - processedAt: DateTime
  - forwardedAt: DateTime
  - idempotencyKey: String
  + process(): PaymentResult
  + markForwarded(): void
}
enum PaymentStatus {
  PENDING
  SUCCEEDED
  FAILED
  FORWARDED
  REFUNDED
}
interface PaymentMethod {
  + process(amount: Decimal): PaymentResult
}
class CashPayment {
  + process(amount: Decimal): PaymentResult
}
class CheckPayment {
  - checkNumber: String
  + process(amount: Decimal): PaymentResult
}
class CreditCardPayment {
  - authorizationReference: String
  + process(amount: Decimal): PaymentResult
}
Patient "1" *-- "0..*" HealthProblem : submits
Organizer "1" -- "0..*" HealthProblem : coordinates
Doctor "1" -- "0..*" HealthProblem : currently assigned to
HealthProblem "1" *-- "0..*" Prescription : prescription history
Doctor "1" -- "0..*" Prescription : authors
Organizer "0..1" -- "0..*" Prescription : delivers
Patient "1" -- "0..*" Payment : pays
HealthProblem "1" -- "0..*" Payment : billed case
Organizer "0..1" -- "0..*" Payment : forwards
Payment "1" --> "1" PaymentMethod : delegates processing to
PaymentMethod <|.. CashPayment
PaymentMethod <|.. CheckPayment
PaymentMethod <|.. CreditCardPayment
@enduml
```

### System sequence — patient registration

```plantuml
@startuml
actor Organizer
participant "Hospital System" as System
Organizer -> System: registerPatient(name, email, contactDetails)
System -> System: validateDetails()
alt details are valid and email is unused
  System -> System: generatePatientId()
  System -> System: create account with password setup flow
  System --> Organizer: patientRegistered(patientId)
else details invalid or email already exists
  System --> Organizer: registrationRejected(reason)
end
@enduml
```

The system should send a password-setup invitation instead of a reusable plaintext password.

### System sequence — consultation

```plantuml
@startuml
actor Patient
actor Organizer
actor Doctor
participant "Hospital System" as System
Patient -> System: submitProblem(description)
System -> System: create HealthProblem(PENDING, createdAt)
System --> Organizer: newProblem(problemId)
Organizer -> System: assignDoctor(problemId, doctorId)
System -> System: setStatus(IN_REVIEW)
System --> Doctor: reviewRequest(problemId, description)
Doctor -> System: submitPrescription(problemId, details, validUntil)
System -> System: savePrescription(issuedAt)
System -> System: setStatus(RESOLVED)
System --> Organizer: prescriptionReady(prescriptionId)
Organizer -> System: deliverPrescription(prescriptionId, patientId)
System -> System: record deliveredAt
System --> Patient: prescriptionDelivered(prescription)
@enduml
```

### System sequence — payment and forwarding

```plantuml
@startuml
actor Patient
actor Organizer
participant "Hospital System" as System
participant "Payment Processor" as Processor
Patient -> System: pay(problemId, amount, paymentMethod, idempotencyKey)
System -> System: validate amount and outstanding balance
System -> System: create Payment(PENDING)
System -> Processor: process(amount, paymentMethod, idempotencyKey)
alt processor confirms payment
  Processor --> System: transactionId, success
  System -> System: record success and transactionId
  System --> Patient: receipt
  System --> Organizer: paymentReadyToForward(paymentId)
  Organizer -> System: forwardPayment(paymentId, doctorId)
  System -> System: record transfer and forwardedAt
  System --> Organizer: transferConfirmed
else processor declines or times out
  Processor --> System: failure
  System -> System: record failure
  System --> Patient: paymentFailed
end
@enduml
```

## Design questions

1. **One patient consults multiple doctors:** keep one HealthProblem case and add a Consultation association class between HealthProblem and Doctor. Store each assignment, review note, and outcome there so earlier consultations are retained.
2. **Prescription reuse:** do not reuse a prescription as a new order. Create a separate refill prescription linked to the original with a `refillsPrescriptionId`.
3. **Payment pattern:** use Strategy. Payment delegates to PaymentMethod, and CashPayment, CheckPayment, and CreditCardPayment implement the same operation polymorphically.
4. **Payment integrity:** use a unique idempotency key to prevent duplicate charges, persist provider transaction references, allow only valid status transitions, and atomically record each successful payment and forwarding. Reconcile uncertain transactions with the provider before retrying.

## Assumptions

- One organizer coordinates each case, and one doctor is the active assignee at a time. The Consultation association class can preserve a multi-doctor history.
- A case can have several prescriptions over time. Each issued prescription is immutable; corrections or refills create a new record.
- Payment method strategies do not store card data in the hospital system.
