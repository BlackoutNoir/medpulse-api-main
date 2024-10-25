from sqlalchemy.orm import Session
from models import Appointment
from schema import AppointmentCreate, AppointmentUpdate
from base_Repo import BaseRepo
from typing import List
from datetime import datetime
import uuid


class AppointmentRepo(BaseRepo):
    def __init__(self, db: Session):
        super().__init__(Appointment, db)

    # Additional methods specific to appointments can be added here
    def get_appointments_by_patient(self, patient_id: uuid.UUID) -> List[Appointment]:
        return self.db.query(Appointment).filter(Appointment.patient_id == patient_id).all()

    def get_appointments_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Appointment]:
        return self.db.query(Appointment).filter(
            Appointment.start_date >= start_date, Appointment.end_date <= end_date
        ).all()
