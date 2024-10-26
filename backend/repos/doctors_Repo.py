from sqlalchemy.orm import Session
from backend.models import Doctor
from base_Repo import BaseRepo
from typing import List
import uuid


class DoctorRepo(BaseRepo):
    def __init__(self, db: Session):
        super().__init__(Doctor, db)

    # Additional methods specific to doctors can be added here
    def get_doctors_by_specialization(self, specialization: str) -> List[Doctor]:
        return self.db.query(Doctor).filter(Doctor.specializations == specialization).all()
