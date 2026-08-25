from enum import Enum


class Specialization(str, Enum):
    GENERAL_PHYSICIAN = "General Physician"
    CARDIOLOGIST = "Cardiologist"
    DERMATOLOGIST = "Dermatologist"
    ORTHOPEDIC = "Orthopedic"
    PEDIATRICIAN = "Pediatrician"
    GYNECOLOGIST = "Gynecologist"
    NEUROLOGIST = "Neurologist"
    PSYCHIATRIST = "Psychiatrist"
    OPHTHALMOLOGIST = "Ophthalmologist"
    ENT = "ENT"