# Hospital Management — UML to Python (optional implementation)

This exercise follows the **Practice UML exo** listed on page 68 of the OOP course PDF, which says the paper exercise can then be implemented.

The existing UML solution is in [UML_Exercise_1_Hospital_Management.md](../UML_Exercise_1_Hospital_Management.md).

## Files
- `hospital.py`: Patient, Doctor, Organizer, HealthProblem, Prescription, payment strategies.
- `test_hospital.py`: unit tests written with Python's built-in `unittest` library.

## Run

```bash
python3 Exercise_3_Hospital_Implementation/hospital.py
python3 -m unittest discover -s Exercise_3_Hospital_Implementation -p "test_*.py" -v
```

The model uses inheritance, composition, enumerations and the Strategy pattern.
**Scope:** educational demonstration only; payments are simulated and no clinical data or real payment processing is supported. The idempotency guard is per object, not a persistent multi-request guarantee.
