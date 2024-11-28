from pydantic import BaseModel
from typing import Optional, List
import uuid
from app.db.enums import blood_type as BloodType
from app.entities.user.schema import UserBase
from app.entities.appointment.schema import AppointmentBase


class MedicalHistoryBase(BaseModel):
    blood_type: Optional[BloodType] 
    height: Optional[float] 
    weight: Optional[float] 

# class AppointmentBase(BaseModel):
#     uid: uuid.UUID

class LabTestBase(BaseModel):
    uid: uuid.UUID

class BillBase(BaseModel):
    uid: uuid.UUID

class PrescriptionBase(BaseModel):
    uid: uuid.UUID

class InsuranceBase(BaseModel):
    company: str 
    details: Optional[str] 
    policy_no: int 



class PatientBase(BaseModel):

    uid: uuid.UUID 
    user_uid: uuid.UUID 
    address: Optional[str] 


#Creation

class PatientCreate(PatientBase):
    medical_history: MedicalHistoryBase
    insurance: InsuranceBase  
    pass


#update
class InsuranceUpdate(BaseModel):
    company: Optional[str] 
    details: Optional[str] 
    policy_no: Optional[int]

class PatientUpdate(PatientBase):
    address: Optional[str] 
    insurance: Optional[InsuranceUpdate]

#response 

class MedicalHistoryResponse(MedicalHistoryBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }

class insuranceResponse(InsuranceBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }

class UserResponse(UserBase):
    uid: uuid.UUID
    model_config = {
        "from_attributes": True
    }

class AppointmentResponse(AppointmentBase):
    uid: uuid.UUID
    model_config = {
        "from_attributes": True
    }

class PatientResponse(PatientBase):
    uid: uuid.UUID
    medical_history: MedicalHistoryResponse
    insurance: Optional[InsuranceBase]
    appointments: List[AppointmentResponse]
    lab_tests: List[LabTestBase]
    prescriptions: List[PrescriptionBase]
    bills: List[BillBase]
    user:  UserResponse
    model_config = {
        "from_attributes": True
    }


class PatientFilter(PatientBase):
    address: Optional[str] 
    order_by: Optional[str]