# Exercise 4 — Hospital Management UML (Visual Diagrams)

This is the **visual version** of the existing Hospital Management UML exercise:
[full written UML solution](../UML_Exercise_1_Hospital_Management.md).

GitHub displays the Mermaid blocks below as diagrams (rather than just code).
The icons identify the roles and major domain objects.

## 1. Class diagram: main entities and relationships

```mermaid
classDiagram
    direction LR
    class Patient {
      +String patientId
      +String name
      +String email
      +submitProblem(description)
      +pay(amount, method)
    }
    class Doctor {
      +String doctorId
      +String name
      +String specialty
      +reviewProblem(problem)
      +issuePrescription(problem, details)
    }
    class Organizer {
      +String organizerId
      +String name
      +registerPatient(details)
      +assignDoctor(problem, doctor)
      +deliverPrescription(prescription)
    }
    class HealthProblem {
      +String problemId
      +String description
      +ProblemStatus status
      +updateStatus(status)
    }
    class Prescription {
      +String prescriptionId
      +String details
      +DateTime issuedAt
      +markDelivered()
    }
    class Payment {
      +String paymentId
      +Decimal amount
      +PaymentStatus status
      +process()
    }
    class PaymentMethod {
      <<interface>>
      +process(amount)
    }
    class CashPayment
    class CheckPayment
    class CreditCardPayment

    Patient "1" --> "0..*" HealthProblem : submits
    Organizer "1" --> "0..*" HealthProblem : coordinates
    Doctor "1" --> "0..*" HealthProblem : reviews
    HealthProblem "1" --> "0..*" Prescription : has
    Doctor "1" --> "0..*" Prescription : issues
    Patient "1" --> "0..*" Payment : makes
    HealthProblem "1" --> "0..*" Payment : billed for
    Payment --> PaymentMethod : uses
    PaymentMethod <|.. CashPayment
    PaymentMethod <|.. CheckPayment
    PaymentMethod <|.. CreditCardPayment
```

## 2. Icon-based overview (who does what)

```mermaid
flowchart LR
  P["🧑 Patient"] -->|Submits problem| H["📋 Health Problem"]
  O["🗂️ Organizer"] -->|Assigns case| D["🩺 Doctor"]
  D -->|Reviews| H
  D -->|Issues| RX["💊 Prescription"]
  O -->|Delivers| RX
  RX -->|Received by| P
  P -->|Pays| PAY["💳 Payment"]
  PAY --> METHOD{"⚙️ Payment method"}
  METHOD --> CASH["💵 Cash"]
  METHOD --> CHECK["🧾 Check"]
  METHOD --> CARD["💳 Credit Card"]
  O -->|Forwards successful payment| D
```

## 3. Sequence diagram: consultation and payment

```mermaid
sequenceDiagram
  actor Patient
  participant System as Hospital System
  participant Organizer
  participant Doctor
  participant PaymentMethod

  Patient->>System: Submit health problem
  System->>Organizer: Notify new case
  Organizer->>Doctor: Assign patient case
  Doctor->>System: Review problem
  Doctor->>System: Issue prescription
  System->>Organizer: Prescription ready
  Organizer->>Patient: Deliver prescription
  Patient->>System: Pay amount with selected method
  System->>PaymentMethod: Process payment
  alt Payment succeeds
    PaymentMethod-->>System: Success
    System-->>Patient: Receipt
    System->>Organizer: Notify payment ready
    Organizer->>Doctor: Forward payment
  else Payment fails
    PaymentMethod-->>System: Failure
    System-->>Patient: Payment failed
  end
```

## 4. Sequence diagram: patient registration

```mermaid
sequenceDiagram
  actor Organizer
  participant System as Hospital System
  actor Patient
  Organizer->>System: registerPatient(details)
  System->>System: Validate details
  alt Valid details
    System->>System: Create patient account
    System-->>Organizer: patientRegistered(patientId)
    System-->>Patient: Account setup invitation
  else Invalid or duplicate details
    System-->>Organizer: registrationRejected(reason)
  end
```

## Notes

- This is a UML design exercise, not a production healthcare application.
- A consultation case has one active doctor and one coordinating organizer at a time; the full solution discusses how to extend the model for multiple consultations.
- Payment methods illustrate the Strategy design pattern.
