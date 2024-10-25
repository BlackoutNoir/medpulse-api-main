from sqlalchemy.orm import Session
from models import Patient
from schema import PatientCreate, PatientUpdate
from base_Repo import BaseRepo
from typing import List
import uuid


class PatientRepo(BaseRepo):
    def __init__(self, db: Session):
        super().__init__(Patient, db)

    # Additional methods specific to patients can be added here
    def get_patients_by_name(self, first_name: str, last_name: str) -> List[Patient]:
        return self.db.query(Patient).filter(
            Patient.first_name == first_name, Patient.last_name == last_name
        ).all()
